## Initial set up in Google Cloud Platform (GCP)

First of all, download [SDK](https://cloud.google.com/sdk/docs/install-sdk) for local setup

### *Step 1* Create a new project in GCP 

Go to https://console.cloud.google.com/ and follow the instructions.

### *Step 2* Create a virtual machine (VM) in GCP
  
  *2.1* Compute Engine -> VM instances -> enable Compute Engine API -> Create instance
  
  *2.2* In the creation process, choose:
  
  - the most suitable region for your location (europe-north1-a in my case)
  - E2, e2-standard-4 (4 vCPU, 16 GB memory) as series/machine type
  - Ubuntu 20.04 LTS, 30GB for Boot Disc

### *Step 3* Create and upload to GCP a ssh key to log in to the VM in GCP without typing a password

For Linix and MacOS: `ssh-keygen -t rsa -f ~/.ssh/KEY_FILENAME -C USERNAME -b 2048` (key is generated in ~/.ssh)

For Windows, look for more details here: [Create SSH Keys](https://cloud.google.com/compute/docs/connect/create-ssh-keys)

Next, copy and upload the public ssh key to GCP: Go to GCP -> Compute Engine -> Metadata -> SSH Keys -> Add SSH Key

### (Optional) *Step 4* Configure instance

  *4.1* To simplify the process, it is suggested to install [Anaconda package management](https://www.anaconda.com/products/distribution)

  Go to the bottom of the page and choose version for Linux, x86 architecture (that's what has been chosen for VM instance):

  ```sh
  wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh

  bash Anaconda3-2022.10-Linux-x86_64.sh
  ```

  *4.2* Create config file on the PC to config access to the server (to avoid command to enter the VM)

  Create a file ~/.ssh/config:

  ```sh
  Host de-zoomcamp # name of the VM
        Hostname 35.228.114.109 # external IP of the VM
        User mikhail # user name which was used to generate the ssh key
        IdentityFile ~/.ssh/gcp # path to the ssh key. Note that it has to be absolute path for Windows
  ```

  Now it is possible to ssh to the VM by typing: `ssh de-zoomcamp` (otherwise it is: `ssh -i ~/.ssh/gcp de-zoomcamp`)

### *Step 5* Clone the repo

`git clone https://github.com/MikhailKuklin/data-pipeline-COVID19-monitoring.git`

### *Step 6* Download Terraform 

[Link to Terraform](https://developer.hashicorp.com/terraform/downloads?product_intent=terraform)

Choose Linux/Ubuntu version (AMD64 architecture), copy the link, and download to the VM with ´wget´:

`wget https://releases.hashicorp.com/terraform/1.3.9/terraform_1.3.9_linux_amd64.zip`

Don't forget to unzip it next.

`unzip terraform_1.3.9_linux_amd64.zip`

Confirm that Terraform is installed:

`terraform -version`

If it does not work for you, move terraform:

`sudo mv terraform /usr/local/bin/`

### *Step 7* GCP setup for Terraform

Service account has to be created for Terraform to give it the credentials to required services in GCP.

Easiest option is to use cli:

```sh
gcloud auth login # OAuth to GCP
gcloud config set account `ACCOUNT`
gcloud iam service-accounts create terraform-iam --display-name "terraform-iam" # create service account for Terraform in GCP
```

Next, we have to define the roles:

```sh
gcloud projects add-iam-policy-binding covid19-monitoring-377519 --member="serviceAccount:terraform-iam@covid19-monitoring-377519.iam.gserviceaccount.com" --role="roles/viewer"
```

```sh
gcloud projects add-iam-policy-binding covid19-monitoring-377519 --member="serviceAccount:terraform-iam@covid19-monitoring-377519.iam.gserviceaccount.com" --role="roles/storage.admin"
```

```sh
gcloud projects add-iam-policy-binding covid19-monitoring-377519 --member="serviceAccount:terraform-iam@covid19-monitoring-377519.iam.gserviceaccount.com" --role="roles/storage.objectAdmin"
```

```sh
gcloud projects add-iam-policy-binding covid19-monitoring-377519 --member="serviceAccount:terraform-iam@covid19-monitoring-377519.iam.gserviceaccount.com" --role="roles/storage.bigquery.admin"
```

Create JSON key:

```sh
mkdir .gc

gcloud iam service-accounts keys create .gc/terraform.json --iam-account=terraform-iam@covid19-monitoring-377519.iam.gserviceaccount.com
```

Set the path to json to interact with GCP from local machine:

```sh
  export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"

  # Refresh token/session, and verify authentication
  gcloud auth application-default login
```

It is also possible to do it in GCP UI:

  *7.1* Go to GCP -> IAM & Admin -> Service Account -> Create Service Account
  
  *7.2* Follow the instructions and in the `Role` box choose:
  
  ```sh
  Viewer
  Storage Admin
  Storage Object Admin
  BigQuery Admin
  ```
  
  and then choose `Done`
  
  *7.3* Actions -> Manage keys -> Create new key (JSON)
  
  *7.4* From the command line of your PC, set the path to json to interact with GCP from local machine:
  
  ```sh
  export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"

  # Refresh token/session, and verify authentication
  gcloud auth application-default login
  ```
  
  *7.5* To add generated json file to the server, one can use `sftp`: 

  ```sh
  sftp de-zoomcamp #connect to the server
  mkdir .gc # create directory
  put de_project.json # copy json file
  ```
  
### *Step 8* Install packages to the VM
  
```sh
conda create -name covid_env
conda activate covid_env
conda install pip
pip install -r requirements.txt
```
  
### *Step 9* Prefect setup
  
Run in the command line of VM `prefect orion start` that will start Prefect UI and go to the address given after execution of the command (`http://127.0.0.1:4200` in my case). Note that you also can use Prefect Cloud which will be forever connected to your account.

To allow Prefect orchestrate the pipeline, one has to give permissions to Prefect to access other services. For that, one has to set up `Blocks` in Prefect. The blocks have to be created for:

```sh
GCP Bucket
GitHub
GCP Credentials
```

The easiest way to do that, run the scripts by adding `json` keys:
```sh
python make_gcp_block.py
python make_gh_block.py
python make_dbt_block.py
```

For GCP credentials, one should already have the json file. For GCS, service account has to be created in GCP:

1. IAM & Admin/Service Accounts
2. Role: BigQuery Admin, Storage Admin

Next, save the key and add it to make_gcp_block.py (!NOTE: do not push to GitHub the script with your credentials inside)

## *Step 10* dbt cloud setup
  
To setup dbt cloud with Big Query, follow detailed instructions from [this guideline](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_4_analytics_engineering/dbt_cloud_setup.md)
  
