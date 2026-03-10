#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/../.."
REGION="us-east-1"

API_ID=$(cat "$SCRIPT_DIR/.api_id" 2>/dev/null || echo "")
FUNCTION_NAME=$(cat "$SCRIPT_DIR/.function_name" 2>/dev/null || echo "SimpleFastAPILambda")

if [ -n "$API_ID" ]; then
    echo "==> Deleting REST API ($API_ID)..."
    awslocal apigateway delete-rest-api \
        --rest-api-id "$API_ID" \
        --region "$REGION" 2>/dev/null || echo "    API not found or already deleted"
else
    echo "==> No API ID found, skipping API deletion"
fi

echo "==> Deleting Lambda function ($FUNCTION_NAME)..."
awslocal lambda delete-function \
    --function-name "$FUNCTION_NAME" \
    --region "$REGION" 2>/dev/null || echo "    Function not found or already deleted"

echo "==> Cleaning build artifacts..."
rm -rf "$PROJECT_ROOT/.build"
rm -f "$SCRIPT_DIR/.api_id" "$SCRIPT_DIR/.function_name"

echo ""
echo "=========================================="
echo " LocalStack Teardown Complete!"
echo "=========================================="
