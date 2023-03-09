## Initial set up in Google Cloud Platform (GCP)

### *Step 1* Install Terraform on your local machine

Choose version for your OS: [Link to Terraform](https://developer.hashicorp.com/terraform/downloads?product_intent=terraform)

Don't forget to unzip it next (MacOS/Linux): `unzip terraform_1.3.9_linux_amd64.zip`

Confirm that Terraform is installed: `terraform -version`

FOr MacOS/Linux, if it does not work for you, move terraform: `sudo mv terraform /usr/local/bin/`

### *Step 2* Create a new project in GCP UI

Go to https://console.cloud.google.com/ and follow the instructions.

## *Step 3* Install Google SDK on you local machine

Choose the compatible version for your OS: ![Download Google Cloud SDK](https://cloud.google.com/sdk/docs/install)

### *Step 3* Creating recources in GCP using Terraform from local machine

 *3.1* Clone repo
 
 `git clone https://github.com/MikhailKuklin/data-pipeline-COVID19-monitoring.git`

 *3.2* Craete service account 
 
 It has to be created for Terraform to give it the credentials to required services in GCP

 Easiest option is to use cli:

  ```sh
  gcloud auth login # OAuth 2 to GCP
  gcloud config set account `ACCOUNT`
  gcloud iam service-accounts create terraform-iam --display-name "terraform-iam" # create service account for Terraform in GCP
  ```

 Next, we have to define the roles:

  ```sh
  gcloud projects add-iam-policy-binding covid19-monitoring-377519 --member="serviceAccount:terraform-iam@covid19-monitoring-377519.iam.gserviceaccount.com" --role="roles/viewer"
  gcloud projects add-iam-policy-binding covid19-monitoring-377519 --member="serviceAccount:terraform-iam@covid19-monitoring-377519.iam.gserviceaccount.com" --role="roles/storage.admin"
  gcloud projects add-iam-policy-binding covid19-monitoring-377519 --member="serviceAccount:terraform-iam@covid19-monitoring-377519.iam.gserviceaccount.com" --role="roles/storage.objectAdmin"
  gcloud projects add-iam-policy-binding covid19-monitoring-377519 --member="serviceAccount:terraform-iam@covid19-monitoring-377519.iam.gserviceaccount.com" --role="roles/bigquery.admin"
  ```

 NOTE that you have to change `covid19-monitoring-377519` on your project ID in GCP.

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

 *3.3* Create resources
 
 NOTE that you need to change in `variables.tf` at least `variable "project"` and perhaps `variable "region"` and `varaiabel "zone"`
 
 ```sh
 cd data-pipeline-COVID19-monitoring/infrastructure/with_vm
 terraform init
 terraform plan
 terraform apply
 ```

 Terraform will create virtual machine, google cloud storage bucker, and BigQuery dataset for you.

### (Optional) *Step 4* Create and upload to GCP a ssh key to log in to the VM in GCP without typing a password

In order to avoid typing the password to log in to the VM from the local machine, one can create ssh key on the local machine:

For Linix and MacOS: `ssh-keygen -t rsa -f ~/.ssh/KEY_FILENAME -C USERNAME -b 2048` (key is generated in ~/.ssh)

For Windows, look for more details here: [Create SSH Keys](https://cloud.google.com/compute/docs/connect/create-ssh-keys)

Next, copy and upload the public ssh key to GCP: Go to GCP -> Compute Engine -> Metadata -> SSH Keys -> Add SSH Key

### (Optional) *Step 5* ssh config on the local machine for the instance 

Create config file on the PC to config access to the server (to avoid the full command to enter the VM)

Create a file ~/.ssh/config:

  ```sh
  Host de-zoomcamp # name of the VM
        Hostname 35.228.114.109 # external IP of the VM
        User mikhail # user name which was used to generate the ssh key
        IdentityFile ~/.ssh/gcp # path to the ssh key. Note that it has to be absolute path for Windows
  ```

Now it is possible to ssh to the VM by typing: `ssh de-zoomcamp` (otherwise it is: `ssh -i ~/.ssh/gcp de-zoomcamp`)

### *Step 6* Necessary installations on the VM

 *5.1* To simplify the process, it is suggested to install [Anaconda package management](https://www.anaconda.com/products/distribution):

  ```sh
  wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh

  bash Anaconda3-2022.10-Linux-x86_64.sh
  
  source .bashrc
  ```

 *5.2* Clone repo and install packages

```sh
git clone https://github.com/MikhailKuklin/data-pipeline-COVID19-monitoring.git
cd data-pipeline-COVID19-monitoring
conda create -n conda-env
conda install pip
pip install -r requirements.txt
```

### *Step 6* Prefect setup
  
Run in the command line of VM `prefect orion start` that will start Prefect UI and go to the address given after execution of the command (`http://127.0.0.1:4200` in my case). Note that you also can use Prefect Cloud which will be forever connected to your account.

To allow Prefect orchestrate the pipeline, one has to give permissions to Prefect to access other services. For that, one has to set up `Blocks` in Prefect. The blocks have to be created for:

```sh
GCP Bucket
GCP Credentials
dbt
```

The easiest way to do that, run the scripts by adding `json` keys:

```sh
python make_gcp_block.py
python make_dbt_block.py
```

For GCP credentials, one should already have the json file (terraform.json).

Next, save the key and add it to make_gcp_block.py (!NOTE: do not push to GitHub the script with your credentials inside)

## *Step 8* dbt cloud setup
  
To setup dbt cloud with Big Query, follow detailed instructions from [this guideline](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_4_analytics_engineering/dbt_cloud_setup.md)
  
