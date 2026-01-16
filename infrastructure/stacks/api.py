"""
API Stack for Stonksfeed

Creates:
- Lambda function for serving articles
- API Gateway HTTP API
- Outputs for CloudFront integration
"""

import secrets

import aws_cdk as cdk
from aws_cdk import (
    CfnOutput,
    Duration,
    Stack,
    aws_apigatewayv2 as apigwv2,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_logs as logs,
    aws_secretsmanager as secretsmanager,
)
from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
from constructs import Construct


class ApiStack(Stack):
    """
    API infrastructure for Stonksfeed.

    Creates a Lambda-backed HTTP API for serving articles from DynamoDB.
    Includes secret header validation for CloudFront origin protection.
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

        # Generate a random secret for origin verification
        self.origin_verify_secret = secrets.token_urlsafe(32)

        # Store the secret in Secrets Manager for reference
        self.secret = self._create_secret()

        # Create Lambda function
        self.get_articles_fn = self._create_get_articles_lambda()

        # Create HTTP API
        self.http_api = self._create_http_api()

        # Outputs
        self._create_outputs()

    def _create_secret(self) -> secretsmanager.Secret:
        """Create secret for origin verification."""
        return secretsmanager.Secret(
            self,
            "OriginVerifySecret",
            secret_name=f"stonksfeed/{self.env_name}/origin-verify",
            description="Secret header value for CloudFront origin verification",
            secret_string_value=cdk.SecretValue.unsafe_plain_text(
                self.origin_verify_secret
            ),
        )

    def _create_get_articles_lambda(self) -> lambda_.Function:
        """Create Lambda function for getting articles."""
        fn = lambda_.Function(
            self,
            "GetArticlesHandler",
            function_name=f"stonksfeed-get-articles-{self.env_name}",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="handler.lambda_handler",
            code=lambda_.Code.from_asset("lambdas/get_articles"),
            timeout=Duration.seconds(30),
            memory_size=256,
            environment={
                "DYNAMODB_TABLE": self.table_name,
                "ORIGIN_VERIFY_HEADER": "x-origin-verify",
                "ORIGIN_VERIFY_SECRET": self.origin_verify_secret,
            },
            log_retention=logs.RetentionDays.TWO_WEEKS,
        )

        # Grant DynamoDB read permissions
        fn.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "dynamodb:GetItem",
                    "dynamodb:Query",
                    "dynamodb:Scan",
                ],
                resources=[self.table_arn],
            )
        )

        return fn

    def _create_http_api(self) -> apigwv2.HttpApi:
        """Create HTTP API Gateway."""
        # Create Lambda integration
        integration = HttpLambdaIntegration(
            "GetArticlesIntegration",
            self.get_articles_fn,
        )

        # Create HTTP API
        http_api = apigwv2.HttpApi(
            self,
            "ArticlesApi",
            api_name=f"stonksfeed-api-{self.env_name}",
            description="Stonksfeed Articles API",
            cors_preflight=apigwv2.CorsPreflightOptions(
                allow_origins=[
                    "https://stonksfeed.com",
                    "http://localhost:8080",
                    "http://localhost:5173",
                ],
                allow_methods=[apigwv2.CorsHttpMethod.GET],
                allow_headers=["Content-Type"],
                max_age=Duration.hours(1),
            ),
        )

        # Add route - path must match CloudFront behavior pattern /api/*
        http_api.add_routes(
            path="/api/articles",
            methods=[apigwv2.HttpMethod.GET],
            integration=integration,
        )

        return http_api

    def _create_outputs(self) -> None:
        """Create CloudFormation outputs."""
        CfnOutput(
            self,
            "ApiEndpoint",
            value=self.http_api.api_endpoint,
            description="HTTP API endpoint URL",
        )

        CfnOutput(
            self,
            "ApiId",
            value=self.http_api.api_id,
            description="HTTP API ID",
        )

        CfnOutput(
            self,
            "OriginVerifyHeader",
            value="x-origin-verify",
            description="Header name for origin verification",
        )

        CfnOutput(
            self,
            "OriginVerifySecretArn",
            value=self.secret.secret_arn,
            description="ARN of the origin verify secret in Secrets Manager",
        )

        CfnOutput(
            self,
            "LambdaFunctionName",
            value=self.get_articles_fn.function_name,
            description="Lambda function name",
        )
