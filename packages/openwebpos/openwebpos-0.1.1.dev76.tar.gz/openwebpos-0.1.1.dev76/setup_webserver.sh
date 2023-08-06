#!/bin/bash

# Ask the user for the application name
echo "What is the name of your application?"
read -r app_name

# Ask the user for gunicorn workers
echo "How many gunicorn workers do you want to use?"
echo "Recommended: 2 * number of cores + 1"
read -r gunicorn_workers

# Set default gunicorn workers to 3
if [ -z "$gunicorn_workers" ]; then
  gunicorn_workers=3
fi

# Update the server
sudo apt-get update
sudo apt-get upgrade

# Install UFW
sudo apt-get install ufw -y

# Install Python Necessary Packages
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools -y
sudo apt install python3-venv -y

# Install Nginx
sudo apt-get install nginx -y

# Create a new directory for the application and move into it
mkdir "$HOME/$app_name"
cd "$HOME/$app_name" || exit

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

# Create a systemd service file3
sudo touch /etc/systemd/system/"$app_name".service

# Add the following to the systemd service file
echo "[Unit]
      Description=Gunicorn instance to serve $app_name
      After=network.target

      [Service]
      User=$USER
      Group=www-data
      WorkingDirectory=$HOME/$app_name
      Environment='PATH=$HOME/$app_name/venv/bin'
      ExecStart=$HOME/$app_name/venv/bin/gunicorn --workers $gunicorn_workers --bind unix:$app_name.sock -m 007 wsgi:app

      [Install]
      WantedBy=multi-user.target" >/etc/systemd/system/"$app_name".service

# Start Gunicorn service
sudo systemctl start "$app_name"

# Enable Gunicorn service
sudo systemctl enable "$app_name"

# Check the status of the Gunicorn service
sudo systemctl status "$app_name"

# Create a new Nginx configuration file
sudo touch /etc/nginx/sites-available/"$app_name"

# Add the following to the Nginx configuration file
echo "server {
      listen 80;
      server_name $app_name;

      location / {
        include proxy_params;
        proxy_pass http://unix:$HOME/$app_name/$app_name.sock;
      }
    }" >/etc/nginx/sites-available/"$app_name"

# Enable the Nginx configuration file
sudo ln -s /etc/nginx/sites-available/"$app_name" /etc/nginx/sites-enabled

# Check the Nginx configuration file for errors
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# Check the status of Nginx
sudo systemctl status nginx

# Allow Nginx through the firewall
sudo ufw allow 'Nginx Full'

# Ask the user if they want to install Certbot
echo "Do you want to install Certbot?"
echo "This will allow you to use HTTPS"
echo "Type 'y' for yes or 'n' for no"
read -r certbot_install

# Install Certbot if the user wants to
if [ "$certbot_install" = "y" ]; then
  sudo apt-get install software-properties-common -y
  sudo add-apt-repository universe -y
  sudo add-apt-repository ppa:certbot/certbot -y
  sudo apt-get update
  sudo apt-get install certbot python3-certbot-nginx -y
  sudo certbot --nginx -d "$app_name"
fi

# Ask the user if they want to install Fail2Ban
echo "Do you want to install Fail2Ban?"
echo "This will protect your server from brute force attacks"
echo "Type 'y' for yes or 'n' for no"
read -r fail2ban_install

# Install Fail2Ban if the user wants to
if [ "$fail2ban_install" = "y" ]; then
  sudo apt-get install fail2ban -y
  sudo systemctl start fail2ban
  sudo systemctl enable fail2ban
fi

# Tell the user the installation is complete
echo "Installation complete!"

# Tell the user how to access the application
echo "Access your application at http://$app_name or https://$app_name"

# Ask the user if they want to reboot the server
echo "Do you want to reboot the server?"
echo "Type 'y' for yes or 'n' for no"
read -r reboot_server

# Reboot the server if the user wants to
if [ "$reboot_server" = "y" ]; then
  sudo reboot
fi