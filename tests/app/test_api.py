import os
import uuid

import boto3
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

API_NAME = os.environ.get("API_NAME", "SimpleFastAPIGateway")
STAGE_NAME = os.environ.get("STAGE_NAME", "local")
REGION = os.environ.get("REGION", "sa-east-1")
LOCALSTACK_URL = "http://localhost:4566"
RUN_LOCALSTACK_TESTS = os.environ.get("RUN_LOCALSTACK_TESTS", "0") == "1"


@pytest.fixture(scope="module")
def base_url():
    client = boto3.client(
        "apigateway",
        endpoint_url=LOCALSTACK_URL,
        region_name=REGION,
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )
    apis = client.get_rest_apis()
    api_id = None
    for api in apis["items"]:
        if api["name"] == API_NAME:
            api_id = api["id"]
            break
    assert api_id is not None, f"API '{API_NAME}' not found in LocalStack"
    return f"{LOCALSTACK_URL}/restapis/{api_id}/{STAGE_NAME}/_user_request_"


@pytest.mark.skipif(
    not RUN_LOCALSTACK_TESTS,
    reason="LocalStack integration tests run only when RUN_LOCALSTACK_TESTS=1",
)
class TestAPI:
    EXISTING_ITEM_ID = "b11af449-22c7-43db-b0e4-dbfbbe7fdbd7"
    NON_ADMIN_ITEM_ID = "b21af449-22c7-43db-b0e4-dbfbbe7fdbd7"
    DELETE_ITEM_ID = "b31af449-22c7-43db-b0e4-dbfbbe7fdbd7"
    ADMIN_ITEM_ID = "b41af449-22c7-43db-b0e4-dbfbbe7fdbd7"

    def test_get_all_items(self, base_url):
        response = requests.get(f"{base_url}/items/get_all_items")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert isinstance(data["items"], list)
        assert len(data["items"]) > 0

    def test_get_item(self, base_url):
        response = requests.get(f"{base_url}/items/{self.EXISTING_ITEM_ID}")
        assert response.status_code == 200
        data = response.json()
        assert data["item_id"] == self.EXISTING_ITEM_ID
        assert data["item"]["name"] == "Barbie"
        assert data["item"]["item_type"] == "TOY"

    def test_create_item(self, base_url):
        new_id = str(uuid.uuid4())
        body = {
            "item_id": new_id,
            "name": "Integration Test Item",
            "price": 9.99,
            "item_type": "TOY",
            "admin_permission": False,
        }
        response = requests.post(f"{base_url}/items/create_item", json=body)
        assert response.status_code == 201
        data = response.json()
        assert data["item_id"] == new_id
        assert data["item"]["name"] == "Integration Test Item"
        assert data["item"]["price"] == 9.99

    def test_update_item(self, base_url):
        body = {
            "item_id": self.NON_ADMIN_ITEM_ID,
            "name": "Updated Hamburguer",
            "price": 42.00,
            "item_type": "FOOD",
            "admin_permission": False,
        }
        response = requests.put(f"{base_url}/items/update_item", json=body)
        assert response.status_code == 200
        data = response.json()
        assert data["item_id"] == self.NON_ADMIN_ITEM_ID
        assert data["item"]["name"] == "Updated Hamburguer"
        assert data["item"]["price"] == 42.00

    def test_delete_item(self, base_url):
        body = {"item_id": self.DELETE_ITEM_ID}
        response = requests.delete(f"{base_url}/items/delete_item", json=body)
        assert response.status_code == 200
        data = response.json()
        assert data["item_id"] == self.DELETE_ITEM_ID
        assert data["item"]["name"] == "T-shirt"
