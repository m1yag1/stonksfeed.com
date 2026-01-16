#!/usr/bin/env bash
# Build script for packaging stonksfeed for Lambda deployment
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
PACKAGE_DIR="$ROOT_DIR/packages/stonksfeed"
LAMBDA_DIR="$ROOT_DIR/infrastructure/lambdas/fetch_rss"

echo "==> Building stonksfeed package for Lambda..."

# Clean up old package files in Lambda directory
echo "    Cleaning up old package files..."
rm -rf "$LAMBDA_DIR/stonksfeed"
rm -rf "$LAMBDA_DIR/stonksfeed-"*.dist-info 2>/dev/null || true

# Copy the package source to Lambda directory
echo "    Copying stonksfeed package..."
cp -r "$PACKAGE_DIR/src/stonksfeed" "$LAMBDA_DIR/"

# Update requirements.txt to include stonksfeed dependencies
echo "    Updating Lambda requirements.txt..."
cat > "$LAMBDA_DIR/requirements.txt" << 'EOF'
requests>=2.31.0
beautifulsoup4>=4.12.0
python-dateutil>=2.8.0
pytz>=2024.1
boto3>=1.34.0
EOF

echo "==> Build complete!"
echo "    Lambda directory: $LAMBDA_DIR"
echo ""
echo "    To deploy, run:"
echo "    cd infrastructure && ave marbz-admin -- uv run cdk deploy -c stack_type=backend ..."
