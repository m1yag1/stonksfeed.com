"""
CI/CD Stack - IAM User and Permissions for GitHub Actions

Creates an IAM user with permissions for:
- S3 bucket operations (static site content)
- CloudFront distribution management
- CloudFormation stack operations
- CDK bootstrap access
- Lambda function management
- DynamoDB access
"""

import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_secretsmanager as secretsmanager,
)
from constructs import Construct


class CiCdStack(Stack):
    """
    Stack for CI/CD pipeline IAM resources.

    Creates:
    - IAM user for GitHub Actions
    - Access keys stored in Secrets Manager
    - Scoped permissions for deployment
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        project_name: str = "stonksfeed",
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.project_name = project_name

        # Create IAM user for CI/CD pipeline
        self.cicd_user = iam.User(
            self,
            "CiCdUser",
            user_name=f"{project_name}-cicd",
        )

        # Create managed policy for deployment operations
        deployment_policy = iam.ManagedPolicy(
            self,
            "DeploymentPolicy",
            managed_policy_name=f"{project_name}-deployment-policy",
            statements=[
                # S3 - static site bucket operations
                iam.PolicyStatement(
                    sid="S3StaticSiteAccess",
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "s3:GetObject",
                        "s3:PutObject",
                        "s3:DeleteObject",
                        "s3:ListBucket",
                        "s3:GetBucketLocation",
                    ],
                    resources=[
                        f"arn:aws:s3:::{project_name}-site",
                        f"arn:aws:s3:::{project_name}-site/*",
                    ],
                ),
                # CloudFront - cache invalidation and read
                iam.PolicyStatement(
                    sid="CloudFrontAccess",
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "cloudfront:CreateInvalidation",
                        "cloudfront:GetInvalidation",
                        "cloudfront:GetDistribution",
                        "cloudfront:ListDistributions",
                    ],
                    resources=["*"],
                ),
                # CloudFormation - stack operations
                iam.PolicyStatement(
                    sid="CloudFormationAccess",
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "cloudformation:*",
                    ],
                    resources=[
                        f"arn:aws:cloudformation:{self.region}:{self.account}:stack/Stonksfeed-*/*",
                        f"arn:aws:cloudformation:{self.region}:{self.account}:stack/CDKToolkit/*",
                    ],
                ),
                # SSM - CDK bootstrap version parameter
                iam.PolicyStatement(
                    sid="SSMParameterAccess",
                    effect=iam.Effect.ALLOW,
                    actions=["ssm:GetParameter"],
                    resources=[
                        f"arn:aws:ssm:{self.region}:{self.account}:parameter/cdk-bootstrap/*",
                    ],
                ),
                # STS - get caller identity
                iam.PolicyStatement(
                    sid="STSAccess",
                    effect=iam.Effect.ALLOW,
                    actions=["sts:GetCallerIdentity"],
                    resources=["*"],
                ),
            ],
        )

        # Create managed policy for CDK operations
        cdk_policy = iam.ManagedPolicy(
            self,
            "CdkPolicy",
            managed_policy_name=f"{project_name}-cdk-policy",
            statements=[
                # IAM - CDK deployment role assumption
                iam.PolicyStatement(
                    sid="CDKRoleAccess",
                    effect=iam.Effect.ALLOW,
                    actions=["iam:PassRole"],
                    resources=[f"arn:aws:iam::{self.account}:role/cdk-*"],
                ),
                # S3 - CDK bootstrap bucket
                iam.PolicyStatement(
                    sid="CDKBootstrapBucketAccess",
                    effect=iam.Effect.ALLOW,
                    actions=["s3:*"],
                    resources=[
                        f"arn:aws:s3:::cdk-*-assets-{self.account}-{self.region}",
                        f"arn:aws:s3:::cdk-*-assets-{self.account}-{self.region}/*",
                    ],
                ),
                # S3 - create/manage project buckets
                iam.PolicyStatement(
                    sid="S3BucketManagement",
                    effect=iam.Effect.ALLOW,
                    actions=["s3:*"],
                    resources=[f"arn:aws:s3:::{project_name}-site"],
                ),
                # CloudFront - create/manage distributions
                iam.PolicyStatement(
                    sid="CloudFrontManagement",
                    effect=iam.Effect.ALLOW,
                    actions=["cloudfront:*"],
                    resources=["*"],
                ),
                # Lambda - create/manage functions
                iam.PolicyStatement(
                    sid="LambdaManagement",
                    effect=iam.Effect.ALLOW,
                    actions=["lambda:*"],
                    resources=[
                        f"arn:aws:lambda:{self.region}:{self.account}:function:{project_name}-*",
                    ],
                ),
                # DynamoDB - table management
                iam.PolicyStatement(
                    sid="DynamoDBManagement",
                    effect=iam.Effect.ALLOW,
                    actions=["dynamodb:*"],
                    resources=[
                        f"arn:aws:dynamodb:{self.region}:{self.account}:table/stonk_articles_*",
                    ],
                ),
                # EventBridge - schedule rules
                iam.PolicyStatement(
                    sid="EventBridgeManagement",
                    effect=iam.Effect.ALLOW,
                    actions=["events:*"],
                    resources=[
                        f"arn:aws:events:{self.region}:{self.account}:rule/{project_name}-*",
                    ],
                ),
                # IAM - Lambda execution role management
                iam.PolicyStatement(
                    sid="IamLambdaRoleManagement",
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "iam:CreateRole",
                        "iam:DeleteRole",
                        "iam:GetRole",
                        "iam:PutRolePolicy",
                        "iam:DeleteRolePolicy",
                        "iam:AttachRolePolicy",
                        "iam:DetachRolePolicy",
                        "iam:TagRole",
                        "iam:UntagRole",
                        "iam:GetRolePolicy",
                    ],
                    resources=[
                        f"arn:aws:iam::{self.account}:role/{project_name}-*",
                        f"arn:aws:iam::{self.account}:role/Stonksfeed-*",
                    ],
                ),
                # CloudWatch Logs - Lambda logs
                iam.PolicyStatement(
                    sid="CloudWatchLogsAccess",
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "logs:CreateLogGroup",
                        "logs:DeleteLogGroup",
                        "logs:DescribeLogGroups",
                        "logs:PutRetentionPolicy",
                    ],
                    resources=[
                        f"arn:aws:logs:{self.region}:{self.account}:log-group:/aws/lambda/{project_name}-*",
                    ],
                ),
            ],
        )

        # Attach policies to user
        self.cicd_user.add_managed_policy(deployment_policy)
        self.cicd_user.add_managed_policy(cdk_policy)

        # Create access key for the user
        access_key = iam.AccessKey(
            self,
            "CiCdUserAccessKey",
            user=self.cicd_user,
        )

        # Store credentials in Secrets Manager
        self.credentials_secret = secretsmanager.Secret(
            self,
            "CiCdCredentials",
            secret_name=f"{project_name}/cicd/credentials",
            description=f"CI/CD credentials for {project_name} GitHub Actions",
            secret_object_value={
                "access_key_id": cdk.SecretValue.unsafe_plain_text(access_key.access_key_id),
                "secret_access_key": access_key.secret_access_key,
            },
        )

        # Outputs
        cdk.CfnOutput(
            self,
            "CiCdUserName",
            value=self.cicd_user.user_name,
            description="IAM user for GitHub Actions",
        )

        cdk.CfnOutput(
            self,
            "CredentialsSecretName",
            value=self.credentials_secret.secret_name,
            description="Secrets Manager secret name for credentials",
        )

        cdk.CfnOutput(
            self,
            "AccessKeyId",
            value=access_key.access_key_id,
            description="Access Key ID (secret key in Secrets Manager)",
        )
