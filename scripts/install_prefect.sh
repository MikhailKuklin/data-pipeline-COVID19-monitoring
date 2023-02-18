#!/bin/bash
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    software-properties-common \
    python3-dateutil
sudo ln -s /usr/bin/python3 /usr/bin/python
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
PATH="$HOME/.local/bin:$PATH"
export PATH
pip3 install prefect prefect-gcp
prefect cloud login -k pnu_rdR1fh39Q4n3GQEcIt9bLSMAGuzm5N3oSUu1

