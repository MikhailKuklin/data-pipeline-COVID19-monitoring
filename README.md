# covid19_monitoring
WIP Data pipeline for uploading, preprocessing, and visualising COVID19 data 

![Project architecture](images/covid19_monitoring_architecture.png)

### Initial set up in Google Cloud Platform (GCP)

*Step 1* Create a new project in GCP (in https://console.cloud.google.com/)
*Step 2* Create a virtual machine (VM) in GCP
  
  *2.1* Compute Engine -> VM instances -> enable Compute Engine API -> Create instance
  *2.2* In the creation process, choose:
  
  - the most suitable region for your location (europe-north1-a in my case)
  - E2, e2-standard-4 (4 vCPU, 16 GB memory) as series/machine type
  - Ubuntu 20.04 LTS, 30GB for Boot Disc
