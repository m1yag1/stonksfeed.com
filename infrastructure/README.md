# Stonksfeed Infrastructure

AWS CDK infrastructure for stonksfeed.com.

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) for dependency management
- AWS CDK CLI (`npm install -g aws-cdk`)
- AWS credentials configured (via `ave marbz-admin --` or similar)

## Setup

```bash
cd infrastructure
uv sync
```

## Stacks

| Stack | Description | Dependencies |
|-------|-------------|--------------|
| `CiCd` | IAM user and credentials for GitHub Actions | None |
| `Data` | DynamoDB table for articles | None |
| `Backend` | Lambda function + EventBridge schedule for RSS fetching | Data |
| `Static` | S3 bucket, CloudFront, ACM certificate, Route53 | None |

## Deployment Order

**Deploy stacks in this order:**

```bash
# Set common variables
export AWS_ACCOUNT=478643413292
export AWS_REGION=us-east-1

# 1. Bootstrap CDK (first time only)
ave marbz-admin -- uv run cdk bootstrap aws://${AWS_ACCOUNT}/${AWS_REGION}

# 2. Deploy CI/CD stack (creates IAM user for GitHub Actions)
ave marbz-admin -- uv run cdk deploy \
  -c stack_type=cicd \
  -c account=${AWS_ACCOUNT} \
  -c region=${AWS_REGION}

# 3. Deploy Data stack (creates DynamoDB table)
ave marbz-admin -- uv run cdk deploy \
  -c stack_type=data \
  -c environment=production \
  -c account=${AWS_ACCOUNT} \
  -c region=${AWS_REGION}

# 4. Deploy Backend stack (creates Lambda + schedule)
# First get the table outputs from the Data stack
TABLE_NAME=$(ave marbz-admin -- aws cloudformation describe-stacks \
  --stack-name Stonksfeed-Data-Production \
  --query "Stacks[0].Outputs[?OutputKey=='TableName'].OutputValue" \
  --output text)
TABLE_ARN=$(ave marbz-admin -- aws cloudformation describe-stacks \
  --stack-name Stonksfeed-Data-Production \
  --query "Stacks[0].Outputs[?OutputKey=='TableArn'].OutputValue" \
  --output text)

ave marbz-admin -- uv run cdk deploy \
  -c stack_type=backend \
  -c environment=production \
  -c table_name=${TABLE_NAME} \
  -c table_arn=${TABLE_ARN} \
  -c account=${AWS_ACCOUNT} \
  -c region=${AWS_REGION}

# 5. Deploy Static Site stack (creates S3, CloudFront, ACM, Route53)
ave marbz-admin -- uv run cdk deploy \
  -c environment=production \
  -c domain=stonksfeed.com \
  -c hosted_zone_domain=stonksfeed.com \
  -c create_hosted_zone=true \
  -c account=${AWS_ACCOUNT} \
  -c region=${AWS_REGION}
```

## Teardown Order

**Destroy stacks in REVERSE order:**

```bash
export AWS_ACCOUNT=478643413292
export AWS_REGION=us-east-1

# 1. Destroy Static Site stack
ave marbz-admin -- uv run cdk destroy Stonksfeed-Production \
  -c environment=production \
  -c account=${AWS_ACCOUNT} \
  -c region=${AWS_REGION}

# 2. Destroy Backend stack
ave marbz-admin -- uv run cdk destroy Stonksfeed-Backend-Production \
  -c stack_type=backend \
  -c environment=production \
  -c account=${AWS_ACCOUNT} \
  -c region=${AWS_REGION}

# 3. Destroy Data stack
# NOTE: DynamoDB table has RETAIN policy - may need manual deletion
ave marbz-admin -- uv run cdk destroy Stonksfeed-Data-Production \
  -c stack_type=data \
  -c environment=production \
  -c account=${AWS_ACCOUNT} \
  -c region=${AWS_REGION}

# 4. Destroy CI/CD stack (do this last)
ave marbz-admin -- uv run cdk destroy Stonksfeed-CiCd \
  -c stack_type=cicd \
  -c account=${AWS_ACCOUNT} \
  -c region=${AWS_REGION}
```

## Manual Cleanup Notes

Some resources have `RemovalPolicy.RETAIN` and won't be deleted by CDK destroy:

- **S3 Bucket**: Empty first with `aws s3 rm s3://stonksfeed-site --recursive`, then delete with `aws s3 rb s3://stonksfeed-site`
- **DynamoDB Table**: Delete manually via AWS Console or CLI
- **Route53 Hosted Zone**: Delete all non-NS/SOA records first, then delete the zone

## Stack Outputs

After deployment, retrieve outputs:

```bash
# Static site outputs
ave marbz-admin -- aws cloudformation describe-stacks \
  --stack-name Stonksfeed-Production \
  --query "Stacks[0].Outputs"

# CI/CD credentials (retrieve from Secrets Manager)
ave marbz-admin -- aws secretsmanager get-secret-value \
  --secret-id stonksfeed/cicd/credentials
```

## Local Development

```bash
# Synthesize CloudFormation templates
uv run cdk synth -c environment=production -c account=${AWS_ACCOUNT} -c region=${AWS_REGION}

# Show what would change
uv run cdk diff -c environment=production -c account=${AWS_ACCOUNT} -c region=${AWS_REGION}

# List all stacks
uv run cdk list -c account=${AWS_ACCOUNT} -c region=${AWS_REGION}
```
