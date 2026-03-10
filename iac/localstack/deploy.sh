#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/../.."

BUILD_DIR="$PROJECT_ROOT/.build/lambda"
ZIP_PATH="$PROJECT_ROOT/.build/lambda.zip"
FUNCTION_NAME="SimpleFastAPILambda"
API_NAME="SimpleFastAPIGateway"
STAGE_NAME="local"
REGION="sa-east-1"

echo "==> Cleaning build directory..."
rm -rf "$PROJECT_ROOT/.build"
mkdir -p "$BUILD_DIR"

echo "==> Installing dependencies into build directory (linux/amd64)..."
pip install -q \
  --platform manylinux2014_x86_64 \
  --python-version 3.12 \
  --implementation cp \
  --only-binary=:all: \
  -t "$BUILD_DIR" \
  mangum fastapi pydantic

echo "==> Copying application code..."
cp -r "$PROJECT_ROOT/src/"* "$BUILD_DIR/"

echo "==> Creating deployment package (lambda.zip)..."
cd "$BUILD_DIR"
zip -q -r "$ZIP_PATH" .
cd "$PROJECT_ROOT"

echo "==> Creating Lambda function '$FUNCTION_NAME'..."
awslocal lambda create-function \
    --function-name "$FUNCTION_NAME" \
    --runtime python3.12 \
    --handler app.main.handler \
    --zip-file "fileb://$ZIP_PATH" \
    --role arn:aws:iam::000000000000:role/lambda-role \
    --environment "Variables={STAGE=TEST}" \
    --region "$REGION" \
    --timeout 15

echo "==> Waiting for Lambda to be active..."
awslocal lambda wait function-active-v2 \
    --function-name "$FUNCTION_NAME" \
    --region "$REGION" 2>/dev/null || sleep 5

echo "==> Creating REST API '$API_NAME'..."
API_ID=$(awslocal apigateway create-rest-api \
    --name "$API_NAME" \
    --region "$REGION" \
    --query 'id' --output text)

echo "    API ID: $API_ID"

echo "==> Getting root resource ID..."
ROOT_ID=$(awslocal apigateway get-resources \
    --rest-api-id "$API_ID" \
    --region "$REGION" \
    --query 'items[?path==`/`].id' --output text)

echo "    Root Resource ID: $ROOT_ID"

LAMBDA_ARN="arn:aws:lambda:$REGION:000000000000:function:$FUNCTION_NAME"

echo "==> Configuring root resource (/) with ANY method..."
awslocal apigateway put-method \
    --rest-api-id "$API_ID" \
    --resource-id "$ROOT_ID" \
    --http-method ANY \
    --authorization-type NONE \
    --region "$REGION"

awslocal apigateway put-integration \
    --rest-api-id "$API_ID" \
    --resource-id "$ROOT_ID" \
    --http-method ANY \
    --type AWS_PROXY \
    --integration-http-method POST \
    --uri "arn:aws:apigateway:$REGION:lambda:path/2015-03-31/functions/$LAMBDA_ARN/invocations" \
    --region "$REGION"

echo "==> Creating proxy resource {proxy+}..."
PROXY_ID=$(awslocal apigateway create-resource \
    --rest-api-id "$API_ID" \
    --parent-id "$ROOT_ID" \
    --path-part "{proxy+}" \
    --region "$REGION" \
    --query 'id' --output text)

echo "    Proxy Resource ID: $PROXY_ID"

echo "==> Configuring proxy resource with ANY method + Lambda integration..."
awslocal apigateway put-method \
    --rest-api-id "$API_ID" \
    --resource-id "$PROXY_ID" \
    --http-method ANY \
    --authorization-type NONE \
    --region "$REGION"

awslocal apigateway put-integration \
    --rest-api-id "$API_ID" \
    --resource-id "$PROXY_ID" \
    --http-method ANY \
    --type AWS_PROXY \
    --integration-http-method POST \
    --uri "arn:aws:apigateway:$REGION:lambda:path/2015-03-31/functions/$LAMBDA_ARN/invocations" \
    --region "$REGION"

echo "==> Deploying API to stage '$STAGE_NAME'..."
awslocal apigateway create-deployment \
    --rest-api-id "$API_ID" \
    --stage-name "$STAGE_NAME" \
    --region "$REGION"

BASE_URL="http://localhost:4566/restapis/$API_ID/$STAGE_NAME/_user_request_"

echo ""
echo "=========================================="
echo " LocalStack Deploy Complete!"
echo "=========================================="
echo ""
echo " API Base URL:"
echo "   $BASE_URL"
echo ""
echo " Endpoints:"
echo "   GET  $BASE_URL/items/get_all_items"
echo "   GET  $BASE_URL/items/{item_id}"
echo "   POST $BASE_URL/items/create_item"
echo "   PUT  $BASE_URL/items/update_item"
echo "   DEL  $BASE_URL/items/delete_item"
echo ""
echo " Example:"
echo "   curl $BASE_URL/items/get_all_items"
echo ""

echo "$API_ID" > "$SCRIPT_DIR/.api_id"
echo "$FUNCTION_NAME" > "$SCRIPT_DIR/.function_name"
