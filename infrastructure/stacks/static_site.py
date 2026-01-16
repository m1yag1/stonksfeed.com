"""
Static Site Stack for Stonksfeed

Creates:
- S3 bucket for static content (private, OAC access)
- CloudFront distribution
- Optional: ACM certificate and Route53 record for custom domain
- Optional: API Gateway origin with secret header validation
"""

from typing import Any

import aws_cdk as cdk
from aws_cdk import (
    CfnOutput,
    Fn,
    Stack,
    aws_certificatemanager as acm,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
    aws_s3 as s3,
)
from constructs import Construct


class StaticSiteStack(Stack):
    """
    Static site infrastructure for Stonksfeed.

    Deploys a React SPA with:
    - S3 bucket (private) for hosting built assets
    - CloudFront distribution with OAC for secure S3 access
    - Optional: ACM certificate and Route53 record for custom domain
    - Optional: API Gateway origin for /api/* paths with secret header
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        env_name: str,
        domain_name: str | None = None,
        hosted_zone_domain: str | None = None,
        api_endpoint: str | None = None,
        api_origin_secret: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.env_name = env_name
        self.domain_name = domain_name
        self.hosted_zone_domain = hosted_zone_domain
        self.api_endpoint = api_endpoint
        self.api_origin_secret = api_origin_secret

        # Create S3 bucket for static content
        self.bucket = self._create_bucket()

        # Setup domain and certificate if configured
        self.hosted_zone = None
        self.certificate = None
        if self.domain_name and self.hosted_zone_domain:
            create_zone = self.node.try_get_context("create_hosted_zone")
            if create_zone:
                self.hosted_zone = self._create_hosted_zone_with_delegation_set()
            else:
                self.hosted_zone = self._lookup_hosted_zone()
            self.certificate = self._create_certificate()

        # Create CloudFront distribution
        self.distribution = self._create_distribution()

        # Create Route53 record if domain is configured
        if self.hosted_zone and self.domain_name:
            self._create_dns_record()

        # Output stack information
        self._create_outputs()

    def _create_bucket(self) -> s3.Bucket:
        """Create S3 bucket for static site content."""
        return s3.Bucket(
            self,
            "SiteBucket",
            bucket_name="stonksfeed-site",
            removal_policy=cdk.RemovalPolicy.RETAIN,
            auto_delete_objects=False,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
        )

    def _lookup_hosted_zone(self) -> route53.IHostedZone | None:
        """Look up existing Route53 hosted zone for the domain."""
        if not self.hosted_zone_domain:
            return None

        return route53.HostedZone.from_lookup(
            self,
            "HostedZone",
            domain_name=self.hosted_zone_domain,
        )

    def _create_hosted_zone_with_delegation_set(self) -> route53.IHostedZone | None:
        """Create a new Route53 hosted zone."""
        if not self.hosted_zone_domain:
            return None

        delegation_set_id = self.node.try_get_context("delegation_set_id")

        hosted_zone = route53.HostedZone(
            self,
            "HostedZone",
            zone_name=self.hosted_zone_domain,
            comment=f"Hosted zone for Stonksfeed ({self.env_name})",
        )

        if delegation_set_id:
            cfn_zone = hosted_zone.node.default_child
            if cfn_zone and hasattr(cfn_zone, "add_property_override"):
                cfn_zone.add_property_override("DelegationSetId", delegation_set_id)

        CfnOutput(
            self,
            "NameServers",
            value=Fn.join(",", hosted_zone.hosted_zone_name_servers or []),
            description="NS records to configure at domain registrar",
        )

        return hosted_zone

    def _create_certificate(self) -> acm.Certificate | None:
        """Create ACM certificate for the custom domain."""
        if not self.domain_name or not self.hosted_zone:
            return None

        return acm.Certificate(
            self,
            "SiteCertificate",
            domain_name=self.domain_name,
            validation=acm.CertificateValidation.from_dns(self.hosted_zone),
            certificate_name=f"stonksfeed-{self.env_name}-cert",
        )

    def _create_api_origin(self) -> origins.HttpOrigin | None:
        """Create API Gateway origin with custom header."""
        if not self.api_endpoint:
            return None

        # Extract domain from API endpoint URL
        # API endpoint format: https://<api-id>.execute-api.<region>.amazonaws.com
        api_domain = self.api_endpoint.replace("https://", "").replace("http://", "").rstrip("/")

        custom_headers = {}
        if self.api_origin_secret:
            custom_headers["x-origin-verify"] = self.api_origin_secret

        return origins.HttpOrigin(
            api_domain,
            protocol_policy=cloudfront.OriginProtocolPolicy.HTTPS_ONLY,
            custom_headers=custom_headers,
        )

    def _create_distribution(self) -> cloudfront.Distribution:
        """Create CloudFront distribution for the static site."""
        oac = cloudfront.S3OriginAccessControl(
            self,
            "OAC",
            description=f"OAC for Stonksfeed {self.env_name}",
        )

        s3_origin = origins.S3BucketOrigin.with_origin_access_control(
            self.bucket,
            origin_access_control=oac,
            origin_path=f"/{self.env_name}",
        )

        # Additional behaviors for API
        additional_behaviors: dict[str, cloudfront.BehaviorOptions] = {}

        api_origin = self._create_api_origin()
        if api_origin:
            additional_behaviors["/api/*"] = cloudfront.BehaviorOptions(
                origin=api_origin,
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_ALL,
                cache_policy=cloudfront.CachePolicy.CACHING_DISABLED,
                origin_request_policy=cloudfront.OriginRequestPolicy.ALL_VIEWER_EXCEPT_HOST_HEADER,
            )

        distribution_props: dict[str, Any] = {
            "default_behavior": cloudfront.BehaviorOptions(
                origin=s3_origin,
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD,
            ),
            "additional_behaviors": additional_behaviors,
            "default_root_object": "index.html",
            "comment": f"Stonksfeed - {self.env_name}",
            "error_responses": [
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=cdk.Duration.seconds(0),
                ),
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=cdk.Duration.seconds(0),
                ),
            ],
        }

        if self.domain_name and self.certificate:
            distribution_props.update(
                {
                    "domain_names": [self.domain_name],
                    "certificate": self.certificate,
                }
            )

        return cloudfront.Distribution(
            self,
            "Distribution",
            **distribution_props,
        )

    def _create_dns_record(self) -> None:
        """Create Route53 alias record pointing to CloudFront."""
        if not self.hosted_zone or not self.domain_name:
            return

        route53.ARecord(
            self,
            "SiteAliasRecord",
            zone=self.hosted_zone,
            record_name=self.domain_name,
            target=route53.RecordTarget.from_alias(
                route53_targets.CloudFrontTarget(self.distribution)
            ),
        )

    def _create_outputs(self) -> None:
        """Create CloudFormation outputs."""
        CfnOutput(
            self,
            "BucketName",
            value=self.bucket.bucket_name,
            description="S3 bucket name for static assets",
        )

        CfnOutput(
            self,
            "EnvPrefix",
            value=self.env_name,
            description="Environment prefix for S3 content",
        )

        CfnOutput(
            self,
            "DistributionId",
            value=self.distribution.distribution_id,
            description="CloudFront distribution ID",
        )

        CfnOutput(
            self,
            "DistributionDomainName",
            value=self.distribution.distribution_domain_name,
            description="CloudFront distribution domain name",
        )

        if self.domain_name:
            CfnOutput(
                self,
                "SiteUrl",
                value=f"https://{self.domain_name}",
                description="Custom domain URL",
            )
        else:
            CfnOutput(
                self,
                "SiteUrl",
                value=f"https://{self.distribution.distribution_domain_name}",
                description="Site URL (CloudFront)",
            )

        if self.api_endpoint:
            CfnOutput(
                self,
                "ApiPath",
                value=f"https://{self.domain_name or self.distribution.distribution_domain_name}/api/articles",
                description="API endpoint through CloudFront",
            )
