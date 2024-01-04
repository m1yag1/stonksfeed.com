import os
import boto3


def upload_site(build_path):
    # Connect to S3
    s3 = boto3.client("s3", region_name="us-east-1")

    # Upload Files Recursively
    bucket_name = "stonksfeed"

    for root, dirs, files in os.walk(build_path):
        for file in files:
            file_path = os.path.join(root, file)
            key = file_path[len(build_path) + 1:]  # Remove the build path prefix

            content_type = get_content_type(file)  # Helper function to get content type based on file extension

            s3.upload_file(
                file_path,
                bucket_name,
                key,
                ExtraArgs={"ContentType": content_type},
            )


def get_content_type(file_path):
    # Map file extensions to content types
    content_types = {
        ".html": "text/html",
        ".css": "text/css",
        ".js": "application/javascript",
        ".png": "image/png",
        # Add more file extensions and content types as needed
    }

    extension = os.path.splitext(file_path)[1]

    return content_types.get(extension.lower(), "application/octet-stream")


if __name__ == "__main__":
    site_path = os.getcwd()
    build_path = os.path.join(site_path, "_build")

    upload_site(build_path)
