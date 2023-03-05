## Initial set up in Google Cloud Platform (GCP)

First of all, download [SDK](https://cloud.google.com/sdk/docs/install-sdk) for local setup

### *Step 1* Create a new project in GCP 

Go to https://console.cloud.google.com/ and follow the instructions.

### *Step 2* GCP setup for Terraform

Service account has to be created for Terraform to give it the credentials to required services in GCP.

  *2.1* Go to GCP -> IAM & Admin -> Service Account -> Create Service Account
  
  *2.2* Follow the instructions and in the `Role` box choose:
  
  ```sh
  Viewer
  Storage Admin
  Storage Object Admin
  BigQuery Admin
  ```
  
  and then choose `Done`
  
  *2.3* Actions -> Manage keys -> Create new key (JSON)
  
  *2.4* From the command line of your PC, set the path to json to interact with GCP from local machine:
  
  ```sh
  export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"

  # Refresh token/session, and verify authentication
  gcloud auth application-default login
  ```
  
  *2.5* To add generated json file to the server, one can use `sftp`: 

  ```sh
  sftp de-zoomcamp #connect to the server
  mkdir .gc # create directory
  put de_project.json # copy json file
  ```

### *Step 3* Create infrastucture using Terraform

  On your laptop:

  *3.1* Go to `/infrastructure` and add to `variables.tf` the name of your project instead of `prime-framing-374716`. Also, change the region if needed.
  
  *3.2* Run the following commands:
  
  ```sh
  terraform init
  terraform plan
  terraform apply
  ```

  It will create the resources in GCP: virtual machine (VM), bucket, BigQuery dataset, and setup region and storage class.
 
### *Step 4* Configure GCP virtual machine (VM)
 
 Go to GCP console -> Compute Engine -> VM Instances -> Open in browser window:
 
  *4.1* Clone the repo

  `git clone https://github.com/MikhailKuklin/data-pipeline-COVID19-monitoring.git`

  *4.2* Go to `/scripts` and run:
  
  `bash setup_vm.sh`
  
  It will download and install Anaconda, Terraform, and packages from requirements.txt necessary for the project.

### *Step 5* Create and upload to GCP a ssh key to log in to the VM in GCP without typing a password

For Linix and MacOS: `ssh-keygen -t rsa -f ~/.ssh/KEY_FILENAME -C USERNAME -b 2048` (key is generated in ~/.ssh)

For Windows, look for more details here: [Create SSH Keys](https://cloud.google.com/compute/docs/connect/create-ssh-keys)

Next, copy and upload the public ssh key to GCP: Go to GCP -> Compute Engine -> Metadata -> SSH Keys -> Add SSH Key

### (Optional) *Step 5* Configure instance

  Create config file on the PC to config access to the server (to avoid command to enter the VM)

  Create a file ~/.ssh/config:

  ```sh
  Host covid19-vm # name of the VM
        Hostname 35.228.114.109 # external IP of the VM
        User mikhail # user name which was used to generate the ssh key
        IdentityFile ~/.ssh/gcp # path to the ssh key. Note that it has to be absolute path for Windows
  ```

  Now it is possible to ssh to the VM by typing: `ssh covid19-vm` (otherwise it is: `ssh -i ~/.ssh/gcp de-zoomcamp`)
  
### *Step 6* Prefect setup
  
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

## *Step 7* dbt cloud setup
  
To setup dbt cloud with Big Query, follow detailed instructions from [this guideline](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_4_analytics_engineering/dbt_cloud_setup.md)
  
  
