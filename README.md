# covid19_monitoring
WIP Data pipeline for uploading, preprocessing, and visualising COVID19 data 

![Project architecture](images/covid19_monitoring_architecture.png)

### Initial set up in Google Cloud Platform (GCP)

*Step 1* Create a new project in GCP (in https://console.cloud.google.com/)

*Step 2* Create and upload to GCP a ssh key to log in to the VM in GCP without typing a password

For Linix and MacOS: `ssh-keygen -t rsa -f ~/.ssh/KEY_FILENAME -C USERNAME -b 2048` (key is generated in ~/.ssh)

For Windows, look for more details here: [Create SSH Keys](https://cloud.google.com/compute/docs/connect/create-ssh-keys)

Next, copy and upload the public ssh key to GCP: Go to GCP -> Compute Engine -> Metadata -> SSH Keys -> Add SSH Key

*Step 3* Create a virtual machine (VM) in GCP
  
  *3.1* Compute Engine -> VM instances -> enable Compute Engine API -> Create instance
  
  *3.2* In the creation process, choose:
  
  - the most suitable region for your location (europe-north1-a in my case)
  - E2, e2-standard-4 (4 vCPU, 16 GB memory) as series/machine type
  - Ubuntu 20.04 LTS, 30GB for Boot Disc

*Step 4* Configure instance

(Optional) *4.1* To simplify the process, it is suggested to install [Anaconda package management] (https://www.anaconda.com/products/distribution)

Go to the bottom of the page and choose version for Linux, x86 architecture (that's what has been chosen for VM instance):

```sh
wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh

bash Anaconda3-2022.10-Linux-x86_64.sh
```



