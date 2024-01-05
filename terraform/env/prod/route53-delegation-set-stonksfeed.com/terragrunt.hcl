terraform {
  source = "${get_terragrunt_dir()}/../../../aws//route53-delegation-set"
}

include {
  path = find_in_parent_folders()
}

inputs = {
    reference_name = "stonksfeed"
}
