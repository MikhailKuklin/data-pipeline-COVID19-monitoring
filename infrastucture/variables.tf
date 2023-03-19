locals {
  data_lake_bucket = "dtc_data_lake2"
}

variable "project" {
  default = "prime-framing-374716"
  type = string
}

variable "region" {
  description = "Region for GCP resources"
  type = string
}

variable "storage_class" {
  description = "Storage class type for your bucket"
  default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "covid"
}

variable "instance" {
  type = string
  default = "covid19_vm"
}

variable "machine_type" {
  type = string
  default = "n1-standard-1"
}

variable "zone" {
  description = "Region for VM"
  type = string
  default = "europe-west6-a"
}