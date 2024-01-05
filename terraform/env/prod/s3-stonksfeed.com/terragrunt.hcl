terraform {
  source = "${get_terragrunt_dir()}/../../../aws/modules//s3"
}

include {
  path = find_in_parent_folders()
}

inputs = {
    bucket_name = "stonksfeed-prod"
}
