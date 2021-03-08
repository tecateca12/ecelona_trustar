# Trustar challenge - Custom QA automation framework + Tests


## Quickstart

### Requirements

#### UBUNTU Local solution

- Python 3 (developed and tested under v 3.6.9)
- Git
- OS dependencies
- All Python library dependencies (included in *requirements.txt*).

#### Ubuntu - Docker solution
- Git
- Docker (developed and tested under v 19.03.10)
  - https://docs.docker.com/engine/install/ubuntu/

### Deployment

To deploy the tool:

1. Clone the repository.
2. Fill out "config.json" to specify how to run tests
3. For local execution make sure that all dependencies are satisfied, from project path root, run on terminal:

```shell
# Install OS dependencies
sudo apt-get update && install_packages \
	python \
	python-dev \
  python3-dev \
	python3-virtualenv \
	python3-pip \
	virtualenv \
	git \
	libnss3 \
	xvfb \
  ffmpeg \
	gcc \
  wget \
  bzip2 \
  chromium \
  chromium-driver \
  curl \
  unzip \
  ca-certificates
sudo apt install git
sudo apt install libnss3
sudo apt install chromium-driver
sudo apt install chromium-browser
sudo apt install ffmpeg
sudo apt-get install xvfb
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
sudo apt install python3-pip

sudo pip install --upgrade pip # If youre running Ubuntu 18 or greater, use pip3 instead of pip: "sudo pip3 install --upgrade pip"

sudo pip install virtualenv # If youre running Ubuntu 18 or greater, use pip3 instead of pip: "sudo pip3 install virtualenv"

virtualenv --python=python3 .env

.env/bin/python -m pip install python-Levenshtein
.env/bin/python -m pip install lxml

.env/bin/python -m pip install -r requirements.txt

```
4. Test everything works by running a test "python runner.py <testpath>"
5. For Docker execution just to have docker installed is required, all dependencies are being satisfied while building the image.

## Local execution
1. From project path root, run on terminal:
```shell
source .env/bin/activate
python runner.py  $testpath -e $environment
```
## Local execution examples:

### Full suite
```shell
source .env/bin/activate
python runner.py Tests -e prod -b chrome 
```
### API test
```shell
source .env/bin/activate
python runner.py Tests/API -e prod -b chrome 
```
### UI test
```shell
source .env/bin/activate
python runner.py Tests/UI -e prod -b chrome 
```

## Docker execution examples:
1. Build image - From project path root, run on terminal:
```shell
sudo docker build -t trustar_docker .
```
2. Run tests
### Full suite
```shell
sudo docker run --shm-size=2g  -e 'environment=prod' -e 'testpath=Tests' --privileged --mount type=bind,source="$(pwd)"/reports,target=/container/reports -it trustar_docker:latest
```
### API test
```shell
sudo docker run --shm-size=2g  -e 'environment=prod' -e 'testpath=Tests/API' --privileged --mount type=bind,source="$(pwd)"/reports,target=/container/reports -it trustar_docker:latest
```
### UI test
```shell
sudo docker run --shm-size=2g  -e 'environment=prod' -e 'testpath=Tests/UI' --privileged --mount type=bind,source="$(pwd)"/reports,target=/container/reports -it trustar_docker:latest

```
## Reports
- Either running on local or docker, the test results will be available under **/reports**.
- Old result executions are moved automatically to **/reports/history** each time the runner is triggered
- API test serves an additional **API_logs_{timestamp}.txt** with details about the requests.
- OPTIONAL: 
  - Results can be opened from html file or mounted to localhost.
     ``` shell
    python3 -m http.server --cgi 4000 #If port 4000 is already in use, it must be replaced for another one
    ```
    - Then open on your browser **http://localhost:4000/reports/**

## Tool structure

The tool is structured with 4 core sections that are worth explaining:

1. Tests folder
2. Libs folder
3. runner.py (the entry point)

### Libs folder

The Libs folder holds all methods, libraries, and utils that are useful to automate any process required, together with driver support, and other configuration setup are stored and managed within the libs folder. 

### runner.py (the entry point)

There is a need to import all necessary libraries and modules together with filtering the tests and also producing reports. All peripheric matters are handled within the entry point of the tool: **runner.py**. After setting up the test run, the script runs each test separately and produces an output with the test results.

#### How the configuration of the tool works

The tool variables can be set up in two different ways:

1. Providing a **config.json** file: the script will look for this file to set up the testing environment.
```
{
  "BROWSER": str,
  "URL_FOR_ENV": {
    "prod": str
  },
  "ENV": str,
  "API_KEY": str,
  "API_URL": str,
  "VIRTUAL_DISPLAY": bool,
  "HEADLESS": bool,
  "BROWSER_WIDTH": int,
  "BROWSER_HEIGHT": int
}

```
2. Some ARGS can be configured directly with the command line and will override the **config.json** file: The tool has a selection of changes that can be included when executing the script. For more information, you can access its help option

```shell
usage: runner.py [-h] [-V] [-e ENV]
                   path [path ...]

USAGE

positional arguments:
  path                  paths to folder(s) with source file(s) [default:
                        Tests]

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -e ENV, --env ENV     select the environment to run tests (just prod implemented for this challenge)
  -b BROWSER, --browser BROWSER  select the browser to run tests (just chrome impleented for this challenge)

```

