locals {
  vars        = read_terragrunt_config("../env_vars.hcl")
  secret_vars = try(read_terragrunt_config("../secret_env_vars.hcl"), { inputs = {} })
}

inputs = merge(
  local.vars.inputs,
  local.secret_vars.inputs,
  {
    region                    = "us-east-1"
  }
)

remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    encrypt        = true
    bucket         = "stonksfeed-${local.vars.inputs.env}-tf"
    dynamodb_table = "terraform-state-lock-dynamo"
    region         = "us-east-1"
    key            = "${path_relative_to_include()}/terraform.tfstate"
  }
}

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite"
  contents  = file("./common/provider.tf")
}

generate "common_variables" {
  path      = "common_variables.tf"
  if_exists = "overwrite"
  contents  = file("./common/common_variables.tf")
}
