include {
  path = find_in_parent_folders()
}

terraform {
  source = "${get_terragrunt_dir()}/../../../aws/modules//s3"
}

inputs = {
    bucket_name = "stonksfeed-prod"
}
