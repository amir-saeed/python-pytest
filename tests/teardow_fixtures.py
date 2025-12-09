import pytest

@pytest.fixture
def temp_file():
    # SETUP: Code before yield
    filename = "test_data.txt"
    with open(filename, "w") as f:
        f.write("Hello World")
    print(f"✅ Created file: {filename}")
    
    # Give the filename to the test
    yield filename
    
    # TEARDOWN: Code after yield (runs after test finishes)
    import os
    os.remove(filename)
    print(f"🧹 Deleted file: {filename}")

def test_read_file(temp_file):
    # Test runs here
    with open(temp_file, "r") as f:
        content = f.read()
    assert content == "Hello World"
    # After this, teardown automatically runs!




import pytest

@pytest.fixture
def temp_file(request):
    # SETUP
    filename = "test_data.txt"
    with open(filename, "w") as f:
        f.write("Hello World")
    
    # Register cleanup function
    def cleanup():
        import os
        os.remove(filename)
        print(f"🧹 Cleaned up {filename}")
    
    request.addfinalizer(cleanup)  # Register teardown
    
    return filename  # Use return instead of yield


import pytest
import boto3
from moto import mock_aws

@pytest.fixture
def dynamodb_table():
    """Create a DynamoDB table, then delete it after test"""
    
    # SETUP: Create mock DynamoDB table
    with mock_aws():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        
        table = dynamodb.create_table(
            TableName='Users',
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        
        print("✅ Table created")
        
        yield table  # Give table to test
        
        # TEARDOWN: Delete table
        table.delete()
        print("🧹 Table deleted")


def test_put_item(dynamodb_table):
    # Use the table
    dynamodb_table.put_item(Item={'id': '123', 'name': 'John'})
    
    # Verify
    response = dynamodb_table.get_item(Key={'id': '123'})
    assert response['Item']['name'] == 'John'
    # Table automatically deleted after this!