"""
Data Stack for Stonksfeed

Creates:
- DynamoDB table for storing articles
"""

import aws_cdk as cdk
from aws_cdk import (
    CfnOutput,
    Stack,
    aws_dynamodb as dynamodb,
)
from constructs import Construct


class DataStack(Stack):
    """
    Data infrastructure for Stonksfeed.

    Creates DynamoDB table for article storage with:
    - Partition key: headline (String)
    - Sort key: pubdate (Number)
    - On-demand billing
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        env_name: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.env_name = env_name

        # Create DynamoDB table for articles
        self.articles_table = dynamodb.Table(
            self,
            "ArticlesTable",
            table_name=f"stonk_articles_{env_name}_table",
            partition_key=dynamodb.Attribute(
                name="headline",
                type=dynamodb.AttributeType.STRING,
            ),
            sort_key=dynamodb.Attribute(
                name="pubdate",
                type=dynamodb.AttributeType.NUMBER,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=cdk.RemovalPolicy.RETAIN,
        )

        # Outputs
        CfnOutput(
            self,
            "TableName",
            value=self.articles_table.table_name,
            description="DynamoDB table name for articles",
        )

        CfnOutput(
            self,
            "TableArn",
            value=self.articles_table.table_arn,
            description="DynamoDB table ARN",
        )
