"""
Backend Stack for Stonksfeed

Creates:
- Lambda function for RSS fetching
- EventBridge rule for scheduled execution
"""

import aws_cdk as cdk
from aws_cdk import (
    CfnOutput,
    Duration,
    Stack,
    aws_events as events,
    aws_events_targets as targets,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_logs as logs,
)
from constructs import Construct


class BackendStack(Stack):
    """
    Backend infrastructure for Stonksfeed.

    Creates Lambda function that fetches RSS feeds and stores articles
    in DynamoDB, triggered by EventBridge schedule.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        env_name: str,
        table_name: str,
        table_arn: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.env_name = env_name
        self.table_name = table_name
        self.table_arn = table_arn

        # Create Lambda function for RSS fetching
        self.fetch_rss_fn = self._create_fetch_rss_lambda()

        # Create EventBridge schedule
        self._create_schedule()

        # Outputs
        self._create_outputs()

    def _create_fetch_rss_lambda(self) -> lambda_.Function:
        """Create Lambda function for fetching RSS feeds."""
        fn = lambda_.Function(
            self,
            "FetchRssHandler",
            function_name=f"stonksfeed-fetch-rss-{self.env_name}",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="handler.lambda_handler",
            code=lambda_.Code.from_asset("lambdas/fetch_rss"),
            timeout=Duration.seconds(60),
            memory_size=256,
            environment={
                "DYNAMODB_TABLE": self.table_name,
            },
            log_retention=logs.RetentionDays.TWO_WEEKS,
        )

        # Grant DynamoDB permissions
        fn.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "dynamodb:PutItem",
                    "dynamodb:GetItem",
                    "dynamodb:Query",
                    "dynamodb:Scan",
                ],
                resources=[self.table_arn],
            )
        )

        return fn

    def _create_schedule(self) -> None:
        """Create EventBridge schedule rule for RSS fetching."""
        # Schedule: Every 3 hours on weekdays
        schedule_rule = events.Rule(
            self,
            "FetchRssSchedule",
            rule_name=f"stonksfeed-fetch-rss-{self.env_name}",
            schedule=events.Schedule.cron(
                minute="0",
                hour="0-23/3",
                week_day="MON-FRI",
            ),
            description="Trigger RSS fetch Lambda every 3 hours on weekdays",
        )

        schedule_rule.add_target(targets.LambdaFunction(self.fetch_rss_fn))

    def _create_outputs(self) -> None:
        """Create CloudFormation outputs."""
        CfnOutput(
            self,
            "FetchRssLambdaName",
            value=self.fetch_rss_fn.function_name,
            description="Lambda function name for RSS fetching",
        )

        CfnOutput(
            self,
            "FetchRssLambdaArn",
            value=self.fetch_rss_fn.function_arn,
            description="Lambda function ARN",
        )
