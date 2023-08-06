[![Python application](https://github.com/baezfb/OpenWebPOS/actions/workflows/python-app.yml/badge.svg)](https://github.com/baezfb/OpenWebPOS/actions/workflows/python-app.yml)
[![Dependency Review](https://github.com/baezfb/OpenWebPOS/actions/workflows/dependency-review.yml/badge.svg)](https://github.com/baezfb/OpenWebPOS/actions/workflows/dependency-review.yml)
# OpenWebPOS

OpenWebPOS is a web-based point of sale system written in python using the Flask framework.

## Installation

### Step 1 - Setting Up Python3

#### Update System
```bash
$ sudo apt update
$ sudo apt -y upgrade
```

#### Check Python Version (3.8)
```bash
$ python3 -V
```

#### Install pip
```bash
$ sudo apt install -y python3-pip
```
Development tools.
```bash
$ sudo apt install build-essential libssl-dev libffi-dev python-dev
```

### Sep 2 - Setting up Virtual environment using venv

```bash
$ sudo apt install -y python3-venv
```

create a project directory. change dirname to your projectname

```bash
$ mkdir dirname
```

```bash
$ cd  dirname
```

create virtual environment

```bash
$ python3 -m venv venv
```

### Step 3 - Activate Virtual Environment

```bash
$ source /vnev/bin/activate
```

### Step 4 - Install
```bash
$ pip install openwebpos
```

## Usage

### Create a app.py file

```python
from openwebpos import open_web_pos
from dotenv import load_dotenv

load_dotenv('.env')  # take environment variables from .env file.

application = open_web_pos()

if __name__ == "__main__":
    application.run()
```

### Run the app

```bash
$ python3 app.py
```

# Developing

To install openwebpos, along with the tools you need to develop and run tests, run the following in your virtualenv:

```bash
$ pip install -e .[dev]
```