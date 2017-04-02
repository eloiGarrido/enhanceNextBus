#!/usr/bin/env bash

# Server and dependencies installation script

# Functions ==================================================================
function install
{
    echo "============> Installing $1..."
    dpkg -s $1 > /dev/null 2>&1
    if [ $? = 0 ]; then
        echo "   ---------> $1 is already installed."
    else
        echo "   ---------> Installation in progress."
        sudo apt-get install -y $1
        echo "   ---------> Installation complete."
    fi
}

function pip_install
{
    echo "============> Installing $1..."
    pip3 freeze | grep $1 > /dev/null 2>&1
    if [ $? = 0 ]; then
        echo "   ---------> $1 is already installed."
    else
        echo "   ---------> Installation in progress."
        sudo pip3 install $1
        echo "   ---------> Installation complete."
    fi
}


function install_dependencies
{
    print_section "REQUIREMENTS INSTALLATION"
    echo "============> Installing dependencies"
    while read line; do install "$line"; done < $FILEDIR/requirements.txt
    printf "\n"

    echo "============> Installing pip dependencies"
    while read line; do pip_install "$line"; done < $FILEDIR/requirements-pip.txt

}

# Run =========================================================================
FILEDIR="$(dirname "$(readlink -f "$0")")"
install_dependencies