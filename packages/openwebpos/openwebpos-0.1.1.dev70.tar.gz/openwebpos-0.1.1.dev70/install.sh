#!/bin/bash

# Default values
app_name="openwebpos"

# Current user
user=$(whoami)

# User home directory
home_dir=$(eval echo ~"$user")

cd "$home_dir" || exit

# Ask for the administrator password upfront
sudo -v

# Keep-alive: update existing `sudo` time stamp until `install.sh` has finished
while true; do
  sudo -n true
  sleep 60
  kill -0 "$$" || exit 0
done 2>/dev/null &

# Update the server
sudo apt update
sudo apt upgrade -y

# Install required packages
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools -y
sudo apt install python3-venv -y
sudo apt install nginx -y

# Ask the user for the application name
echo "What is the name of your application?"
read -r app_name

# Create a new directory for the application and move into it
mkdir "$home_dir/$app_name"
cd "$home_dir/$app_name" || exit

# Create a virtual environment for the application
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the application's dependencies
pip install wheel gunicorn openwebpos --pre

# Create wsgi.py file
touch wsgi.py

# Add the following to the wsgi.py file
echo "from openwebpos import open_web_pos
app = open_web_pos()
if __name__ == '__main__':
    open_web_pos()" >wsgi.py

# Create a systemd service file
sudo touch /etc/systemd/system/"$app_name".service

# Ask the user if they want to set gunicorn workers
echo "Do you want to set gunicorn workers? (y/n)"
select yn in "Yes" "No"; do
  case $yn in
  Yes)
    # Ask the user for gunicorn workers
    echo "How many gunicorn workers do you want to use?"
    echo "Recommended: 2 * number of cores + 1"
    read -r gunicorn_workers

    # Set default gunicorn workers to 3
    if [ -z "$gunicorn_workers" ]; then
      gunicorn_workers=3
    fi
    # Add the following to the systemd service file
    sudo echo "[Unit]
    Description=Gunicorn instance to serve $app_name
    After=network.target
    [Service]
    User=$USER
    Group=www-data
    WorkingDirectory=$HOME/$app_name
    Environment='PATH=$HOME/$app_name/venv/bin'
    ExecStart=$HOME/$app_name/venv/bin/gunicorn --workers $gunicorn_workers --threads 4 --worker-class gevent --timeout 120 --bind 0.0.0.0:$app_port wsgi:app
    [Install]
    WantedBy=multi-user.target" | sudo tee /etc/systemd/system/"$app_name".service
    break
    ;;
  No)
    # Add the following to the systemd service file
    sudo echo "[Unit]
    Description=Gunicorn instance to serve $app_name
    After=network.target
    [Service]
    User=$USER
    Group=www-data
    WorkingDirectory=$HOME/$app_name
    Environment='PATH=$HOME/$app_name/venv/bin'
    ExecStart=$HOME/$app_name/venv/bin/gunicorn --threads 4 --worker-class gevent --timeout 120 --bind 0.0.0.0:$app_port wsgi:app
    [Install]
    WantedBy=multi-user.target" | sudo tee /etc/systemd/system/"$app_name".service
    break
    ;;
  esac
done

# Create an application socket file
sudo touch /etc/systemd/system/"$app_name".socket

# Ask the user for the application port
echo "What port do you want to use for your application?"
read -r app_port

sudo echo "[Unit]
Description=gunicorn socket for $app_name

[Socket]
ListenStream=$app_port
FileDescriptoName=http
# Our service won't need permissions for the socket, since it
# inherits the file descriptor by socket activation
# only the nginx daemon will need access to the socket
SocketUser=www-data
# Optionally restrict the socket permissions even more.
# SocketMode=600
[Install]
WantedBy=sockets.target
" | sudo tee /etc/systemd/system/"$app_name".socket

# Start application service
sudo systemctl start "$app_name".socket
sudo systemctl start "$app_name".service

# Enable application service
sudo systemctl enable "$app_name".socket
sudo systemctl enable "$app_name".service

# Status of application service
sudo systemctl status "$app_name".socket
sudo systemctl status "$app_name".service

# Ask the user if they want to restart the server
echo "Do you want to restart the server? (y/n)"
select yn in "Yes" "No"; do
  case $yn in
  Yes)
    sudo reboot
    break
    ;;
  No)
    echo "Open Web POS is now installed!"
    sleep 3
    exit 0
    ;;
  esac
done
