#!/bin/bash

if [ -z "$PROJECT_ID" ]
  then
    echo "Project ID environment variable missing"
    exit 1
fi


# create roles for service account
gcloud iam service-accounts create sa-iam --display-name "sa-iam" # create service account for Terraform in GCP
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:sa-iam@$PROJECT_ID.iam.gserviceaccount.com" --role="roles/viewer"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:sa-iam@$PROJECT_ID.iam.gserviceaccount.com" --role="roles/storage.admin"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:sa-iam@$PROJECT_ID.iam.gserviceaccount.com" --role="roles/storage.objectAdmin"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:sa-iam@$PROJECT_ID.iam.gserviceaccount.com" --role="roles/bigquery.admin"

# save json key
mkdir .gc
gcloud iam service-accounts keys create ../.gc/sa-iam.json --iam-account=sa-iam@$PROJECT_ID.iam.gserviceaccount.com

# set the path to json to interact with GCP from local machine
export GOOGLE_APPLICATION_CREDENTIALS="../.gc/sa-iam.json"
