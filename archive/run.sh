#!/bin/bash

# echo "starting..."
# Check if the script is run with sudo
if [ "$EUID" -ne 0 ]; then
    echo "This script must be run with sudo or as root."
    exit 1
fi
# Check if the script is called with exactly two arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 Username Password"
    exit 1
fi
# Assign the arguments to variables
arg1="$1"
arg2="$2"
# Rest of your script using arg1 and arg2
cd src/drone
./drone.sh $arg1 $arg2
