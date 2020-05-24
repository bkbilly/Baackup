#!/bin/bash

# Global
basedir=/opt/Baackup

# Installing Dependencies

echo -e "\e[35mLooking for GIT...\e[0m"
if [ -z $(which git) ]; then
    echo -e "\e[31mGit not found, installing from apt-get:\e[0m"
    sudo apt-get --yes --force-yes install git
fi

echo -e "\e[35mLooking for Python3...\e[0m"
if [ -z $(which python3) ]; then
    echo -e "\e[31mPython3 not found, installing from apt-get:\e[0m"
    sudo apt-get --yes --force-yes install python3
fi


echo -e "\e[35mLooking for PIP3...\e[0m"
if [ -z $(which pip3) ]; then
    echo -e "\e[31mPIP3 not found, installing:\e[0m"
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    sudo python3 get-pip.py
fi

# Download from GitHub
if [ ! -d $basedir ]; then
    echo -e "\e[35mDownloading from GitHub:\e[0m"
    sudo git clone https://github.com/bkbilly/Baackup.git $basedir
else
    echo -e "\e[35mRepository already exists, updating...\e[0m"
    sudo git -C $basedir pull origin master
fi

# Install Python requirements
echo -e "\e[35mInstalling Python requirements:\e[0m"
sudo pip3 install -r $basedir/requirements.txt

# Setup
echo -e "\e[35mMigrating Database:\e[0m"
sudo python3 $basedir/manage.py migrate
sudo python3 $basedir/manage.py makemigrations
sudo python3 $basedir/manage.py migrate

# Install as a service
echo -e "\e[35mInstalling as a service...\e[0m"
sudo cp $basedir/autostart/baackup.service /etc/systemd/system/baackup.service
sudo chmod +x /etc/systemd/system/baackup.service
sudo systemctl enable baackup
sudo service baackup start


# Done
myURL="http://localhost:8000"
echo -e "\n\n\nAll done!"
echo -e "\e[33mThis is your URL: $myURL\e[0m"
echo "Enjoy!!!"

