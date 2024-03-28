#!/bin/bash

set -e

UNAME=$(uname -s)

if [ $(python3 -c "import venv" &> /dev/null && echo 1 || echo 0) ]
then
    echo "python3 and venv are available"
elif [ "$UNAME" = "Linux" ]
then
    echo "Installing venv on Linux"
    sudo apt-get install -y python3-venv
fi
if [ "$UNAME" = "Darwin" ]
then
    echo "Installing venv on Darwin"
    brew install python3.11-venv
fi
python3 -m venv .venv && . .venv/bin/activate && pip3 install -r requirements.txt && python3 -m PyInstaller -v && python3 -m PyInstaller --onefile --hidden-import="googleapiclient" src/main.py
tar -czvf dist/archive.tar.gz dist/main
