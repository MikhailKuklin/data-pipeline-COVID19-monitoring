#!/bin/bash

# Download Anaconda3-2022.10-Linux-x86_64.sh
wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh

# Run Anaconda3-2022.10-Linux-x86_64.sh
bash Anaconda3-2022.10-Linux-x86_64.sh

# Download Terraform 1.3.9
wget https://releases.hashicorp.com/terraform/1.3.9/terraform_1.3.9_linux_amd64.zip

# Install unzip
sudo apt install unzip

# Unzip Terraform 1.3.9
unzip terraform_1.3.9_linux_amd64.zip
