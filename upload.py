import os

import boto3


def upload_site(build_path):
    # Connect to S3
    s3 = boto3.client("s3", region_name="us-east-1")

    # Upload File
    bucket_name = "stonksfeed"
    content_type = "text/html"
    s3.upload_file(
        build_path + "/index.html",
        bucket_name,
        "index.html",
        ExtraArgs={"ContentType": content_type},
    )


if __name__ == "__main__":
    site_path = os.getcwd()
    build_path = os.path.join(site_path, "_build")

    upload_site(build_path)
