#!/usr/bin/env python3
"""
Stonksfeed Infrastructure

Stack types:
- cicd: Creates IAM user and credentials for GitHub Actions (deploy first)
- static: Creates S3 + CloudFront for static site hosting
- data: Creates DynamoDB table for articles
- backend: Creates Lambda + EventBridge schedule for RSS fetching
- api: Creates API Gateway + Lambda for serving articles
"""

import aws_cdk as cdk

from stacks import ApiStack, BackendStack, CiCdStack, DataStack, StaticSiteStack


class StonksfeedApp(cdk.App):
    """Main CDK application for Stonksfeed."""

    def __init__(self) -> None:
        super().__init__()

        env_name = self.node.try_get_context("environment") or "production"
        stack_type = self.node.try_get_context("stack_type") or "static"

        # Domain configuration
        domain_name = self.node.try_get_context("domain")
        hosted_zone_domain = self.node.try_get_context("hosted_zone_domain")

        env_config = cdk.Environment(
            account=self.node.try_get_context("account"),
            region=self.node.try_get_context("region") or "us-east-1",
        )

        if stack_type == "cicd":
            CiCdStack(
                self,
                "Stonksfeed-CiCd",
                project_name="stonksfeed",
                env=env_config,
            )
        elif stack_type == "data":
            DataStack(
                self,
                f"Stonksfeed-Data-{env_name.title()}",
                env_name=env_name,
                env=env_config,
            )
        elif stack_type == "backend":
            # Backend stack needs references to data stack outputs
            table_name = self.node.try_get_context("table_name")
            table_arn = self.node.try_get_context("table_arn")
            if not table_name or not table_arn:
                raise ValueError(
                    "table_name and table_arn context values are required for backend stack"
                )
            BackendStack(
                self,
                f"Stonksfeed-Backend-{env_name.title()}",
                env_name=env_name,
                table_name=table_name,
                table_arn=table_arn,
                env=env_config,
            )
        elif stack_type == "api":
            # API stack needs references to data stack outputs
            table_name = self.node.try_get_context("table_name")
            table_arn = self.node.try_get_context("table_arn")
            if not table_name or not table_arn:
                raise ValueError(
                    "table_name and table_arn context values are required for api stack"
                )
            ApiStack(
                self,
                f"Stonksfeed-Api-{env_name.title()}",
                env_name=env_name,
                table_name=table_name,
                table_arn=table_arn,
                env=env_config,
            )
        else:
            # Optional API integration
            api_endpoint = self.node.try_get_context("api_endpoint")
            api_origin_secret = self.node.try_get_context("api_origin_secret")

            StaticSiteStack(
                self,
                f"Stonksfeed-{env_name.title()}",
                env_name=env_name,
                domain_name=domain_name,
                hosted_zone_domain=hosted_zone_domain,
                api_endpoint=api_endpoint,
                api_origin_secret=api_origin_secret,
                env=env_config,
            )


if __name__ == "__main__":
    app = StonksfeedApp()
    app.synth()
