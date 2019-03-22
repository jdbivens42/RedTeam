#!/bin/bash

GIT_DEST='/root/tools/'
INSTALL='apt-get install -y'

export DEBIAN_FRONTEND=noninteractive

mkdir -p $GIT_DEST 

wget -q -O - https://archive.kali.org/archive-key.asc | apt-key add

dpkg --add-architecture i386 && apt-get update

apt update; apt upgrade -y

$INSTALL vim curl net-tools git ftp locate 

$INSTALL binutils dnsutils htop nethogs

$INSTALL screen tmux terminator xclip

$INSTALL ftp lftp rdesktop xvnc4viewer openvpn rsync telnet smbclient

$INSTALL python python-pip python3 python3-pip

$INSTALL nmap zenmap metasploit-framework powersploit armitage mimikatz exploitdb wordlists seclists msfpc xsltproc windows-binaries

$INSTALL hydra dirb gobuster wpscan sqlmap nikto skipfish cutycapt fierce snmp snmpcheck enum4linux dirbuster unicornscan dnsrecon zaproxy onesixtyone

$INSTALL tcpdump wireshark aircrack-ng

$INSTALL john hashcat

$INSTALL unix-privesc-check

$INSTALL webshells apache2 php

$INSTALL radare2 gdb ollydbg

$INSTALL mingw-w64 golang upx

$INSTALL kali-linux-pwtools

$INSTALL burpsuite phantomjs

$INSTALL wine32

# Clean up the papers we don't need
rm -rf /usr/share/exploitdb-papers

# Python Modules
pip install argparse setuptools wheel
pip3 install argparse setuptools wheel
pip install pwntools

# Initialization stuff
searchsploit -u
msfdb init

# Install PowerShell (https://www.kali.org/tutorials/installing-powershell-on-kali-linux/)
# https://www.netsecfocus.com/infosec/tools/2018/09/25/Installing_Powershell_and_Powershell_Preview_on_Kali_Linux_2018-3.html
$INSTALL curl gnupg apt-transport-https
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
echo "deb [arch=amd64] https://packages.microsoft.com/repos/microsoft-debian-stretch-prod stretch main" > /etc/apt/sources.list.d/powershell.list
apt update

wget http://ftp.us.debian.org/debian/pool/main/i/icu/libicu57_57.1-6+deb9u2_amd64.deb
dpkg -i libicu57_57.1-6+deb9u2_amd64.deb

wget http://ftp.us.debian.org/debian/pool/main/i/icu/icu-devtools_57.1-6+deb9u2_amd64.deb
dpkg -i icu-devtools_57.1-6+deb9u2_amd64.deb

wget http://ftp.us.debian.org/debian/pool/main/u/ust/liblttng-ust0_2.9.0-2+deb9u1_amd64.deb
dpkg -i liblttng-ust0_2.9.0-2+deb9u1_amd64.deb

wget http://ftp.us.debian.org/debian/pool/main/libu/liburcu/liburcu4_0.9.3-1_amd64.deb
dpkg -i liburcu4_0.9.3-1_amd64.deb

wget http://ftp.us.debian.org/debian/pool/main/u/ust/liblttng-ust-ctl2_2.9.0-2+deb9u1_amd64.deb
dpkg -i liblttng-ust-ctl2_2.9.0-2+deb9u1_amd64.deb

rm *.deb

$INSTALL powershell

# Powershell Empire
pushd $GIT_DEST
git clone https://github.com/EmpireProject/Empire

pushd Empire
./setup/install.sh
popd

popd

# PEDA
pushd $GIT_DEST
git clone https://github.com/longld/peda.git
echo "source ./peda/peda.py" >> ~/.gdbinit

popd


# AutoBlue
pushd $GIT_DEST
git clone https://github.com/3ndG4me/AutoBlue-MS17-010
popd

# progress bars?
pushd $GIT_DEST
git clone https://github.com/Xfennec/progress
pushd progress
make && make install
popd


# Lazy Script
pushd $GIT_DEST
git clone https://github.com/arismelachroinos/lscript.git
pushd lscript
chmod +x install.sh
./install.sh
popd


# ssh-audit
pushd $GIT_DEST
git clone https://github.com/jtesta/ssh-audit
popd


# httpscreenshot
pushd $GIT_DEST
git clone https://github.com/breenmachine/httpscreenshot
$INSTALL swig swig2.0 libssl-dev python-dev python-pip

pushd httpscreenshot
pip install requirements.txt
popd

wget https://github.com/mozilla/geckodriver/releases/download/v0.11.1/geckodriver-v0.11.1-linux64.tar.gz
tar xzvf geckodriver-v0.11.1-linux64.tar.gz
mv geckodriver /usr/bin/geckodriver
popd

# Web Scanner
pushd $GIT_DEST
$INSTALL python3 python3-pip python3-yaml python3-docopt git
git clone https://github.com/fgeek/pyfiscan

pushd pyfiscan
pip3 install -r requirements.lst
popd

popd


# Windows Enum
pushd $GIT_DEST
git clone https://github.com/411Hall/JAWS
popd

# Windows Enum
pushd $GIT_DEST
git clone https://github.com/pentestmonkey/windows-privesc-check
popd

# Windows Enum
pushd $GIT_DEST
git clone https://github.com/sn0wfa11/win_enum_local
popd

# Linux Enum
pushd $GIT_DEST
git clone https://github.com/rebootuser/LinEnum
popd

# Powershell Framework
pushd $GIT_DEST
git clone https://github.com/samratashok/nishang
popd

# Windows AD Exploitation
pushd $GIT_DEST
git clone https://github.com/hausec/ADAPE-Script
popd

# NoSQLMap
pushd $GIT_DEST
git clone https://github.com/codingo/NoSQLMap
pushd NoSQLMap
python setup.py install
popd
popd

# Some random guy
pushd $GIT_DEST
git clone https://github.com/truongkma/ctf-tools
popd

# Literal Dumpster Fire
pushd $GIT_DEST
git clone https://github.com/jdbivens42/RedTeam
git clone https://github.com/jdbivens42/Executor
git clone https://github.com/jdbivens42/switchblade
git clone https://github.com/jdbivens42/c2Trash

pip install argparse
pip3 install netifaces prompt_toolkit colored libtmux validators multipart argparse ssl

pip3 install pycrypto

go get crypto/tls

pip3 install psutil
$INSTALL cpanminus
cpanm install XML::Simple WWW::Mechanize WWW::Mechanize::Plugin::FollowMetaRedirect

pushd RedTeam/shells

pushd python
make setup
popd

pushd c
make setup
popd

pushd go
make setup
popd

popd
popd


# GHIDRA
$INSTALL openjdk-11-jdk
wget https://ghidra-sre.org/ghidra_9.0_PUBLIC_20190228.zip
unzip ghidra_9.0_PUBLIC_20190228.zip $GIT_DEST

# Interactive

#IDA Pro (Free 7.0)
curl -#LO https://out7.hex-rays.com/files/idafree70_linux.run
chmod +x idafree70_linux.run
./idafree70_linux.run


# Clean up
apt autoremove -y
