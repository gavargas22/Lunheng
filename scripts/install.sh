#!/usr/bin/env bash

# Install dependencies for Lunheng
# =============================================
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

LUNHENG_PATH="~/Lunheng"
IPADDRESS="$(/sbin/ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1)"

#--- Display the 'welcome' splash/user warning info..
echo ""
echo "############################################################"
echo "#  Welcome tot the Lunheng Installer v1.0  #"
echo "############################################################"

echo -e "\nInstalling dependencies"

#--- Prepare for install
sudo apt-get -yqq update   #ensure we can install

# ***************************************
# Installation really starts here

sudo apt-get install -y build-essential libssl-dev libcurl4-gnutls-dev libexpat1-dev gettext unzip

sudo apt-get install -y git

# Install Node
wget http://node-arm.herokuapp.com/node_latest_armhf.deb
sudo dpkg -i node_latest_armhf.deb
# install Bower
sudo npm install -g bower


# Collect the ip address of the RPi
# echo ""
# read -e -p "Enter the ip address of the Raspberry Pi: " PI_ADDRESS

cd $PANEL_PATH

# Install Apache
sudo apt-get install -y apache2
sudo service apache2 restart
# Open Port 80 just in case
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Install mariaDB
sudo apt-get install -y mariadb-server

# Install PHP and dependencies
sudo apt-get install -y php5 libapache2-mod-php5 php5-mcrypt

# Copy the file to apache configuration
sudo cp -f ~/Lunheng/apache_files/dir.conf /etc/apache2/mods-enabled/dir.conf apache_files/dir.conf

# Restart apache
sudo service apache2 restart

# Remove useless things from root folder
sudo rm -rfv /var/www/html/*

# Symlink the files of the app
sudo ln -s ~/Lunheng/* .

# Install pip
sudo apt-get install -y python-pip
# Install Daemon
sudo pip install daemon
# That's it!
