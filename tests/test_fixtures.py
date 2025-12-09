import pytest

@pytest.fixture(scope="function")  # or just @pytest.fixture
def counter():
    print("\n🔧 Creating counter")
    return {"count": 0}

def test_increment_1(counter):
    counter["count"] += 1
    assert counter["count"] == 1
    print(f"Test 1: {counter['count']}")

def test_increment_2(counter):
    counter["count"] += 1
    assert counter["count"] == 1  # Still 1! Fresh counter
    print(f"Test 2: {counter['count']}")


import pytest

@pytest.fixture(scope="class")
def database():
    print("\n🔧 Creating database ONCE for class")
    db = {"users": []}
    return db

class TestUserOperations:
    def test_add_user(self, database):
        database["users"].append("Alice")
        assert len(database["users"]) == 1
        print(f"After add: {database['users']}")
    
    def test_add_another_user(self, database):
        database["users"].append("Bob")
        assert len(database["users"]) == 2  # Alice still there!
        print(f"After add: {database['users']}")



import pytest
import boto3
from moto import mock_aws  # ✅ New import

@pytest.fixture(scope="module")
def dynamodb_table():
    print("\n🔧 Creating DynamoDB table ONCE for module")
    
    with mock_aws():  # ✅ Changed here
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        
        table = dynamodb.create_table(
            TableName='Users',
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        
        yield table  # Tests use this


def test_put_item(dynamodb_table):
    dynamodb_table.put_item(Item={'id': '1', 'name': 'Alice'})
    assert True
    print("✅ Item added")


def test_get_item(dynamodb_table):
    response = dynamodb_table.get_item(Key={'id': '1'})
    assert response['Item']['name'] == 'Alice'
    print(f"✅ Found: {response['Item']['name']}")



# conftest.py (special pytest file)
import pytest

@pytest.fixture(scope="session")
def aws_credentials():
    print("\n🔧 Setting AWS creds ONCE for entire session")
    import os
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    return True

# test_lambda_1.py
def test_lambda_1(aws_credentials):
    print("Test 1 using credentials")

# test_lambda_2.py
def test_lambda_2(aws_credentials):
    print("Test 2 using SAME credentials")
