# Update UBUNTU packages 
sudo apt-get -y update

# Install OS dependencies
sudo apt-get -y install python
sudo apt-get -y install python-dev
sudo apt-get -y install python3-dev
sudo apt-get -y install python3-virtualenv
sudo apt-get -y install python3-pip
sudo apt-get -y install virtualenv
sudo apt-get -y install python3-venv
sudo apt-get -y install git
sudo apt-get -y install libnss3
sudo apt-get -y install xvfb
sudo apt-get -y install ffmpeg
sudo apt-get -y install gcc
sudo apt-get -y install wget
sudo apt-get -y install bzip2
sudo apt-get -y install curl
sudo apt-get -y install unzip
sudo apt-get -y install ca-certificates
sudo apt-get -y install chromium-driver

# Install chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
sudo rm ./google-chrome-stable_current_amd64.deb

sudo apt -y install python3-pip
sudo pip3 install --upgrade pip 
sudo pip3 install virtualenv 

# virtualenv --python=python3 .env
sudo python3 -m venv .env

sudo .env/bin/python -m pip install python-Levenshtein
sudo .env/bin/python -m pip install lxml

sudo .env/bin/python -m pip install -r requirements.txt
