import pytest
import json
import os
from typing import Dict, Any


@pytest.fixture(autouse=True)
def aws_credentials():
    """Set fake AWS credentials for testing"""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture
def lambda_context():
    """Create a mock Lambda context"""
    class MockContext:
        function_name = "test-function"
        memory_limit_in_mb = 128
        invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test-function"
        aws_request_id = "test-request-id"
        
    return MockContext()


@pytest.fixture
def api_gateway_event():
    """Basic API Gateway event structure"""
    return {
        "resource": "/users",
        "path": "/users",
        "httpMethod": "POST",
        "headers": {
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        "queryStringParameters": None,
        "pathParameters": None,
        "body": None,
        "isBase64Encoded": False
    }


@pytest.fixture
def valid_user_data():
    """Valid user data for testing"""
    return {
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    }


@pytest.fixture
def invalid_user_data():
    """Invalid user data (missing email)"""
    return {
        "name": "Jane Doe",
        "age": 25
    }


@pytest.fixture
def api_event_with_valid_user(api_gateway_event, valid_user_data):
    """
    Complex fixture that USES other fixtures!
    This combines api_gateway_event + valid_user_data
    """
    event = api_gateway_event.copy()
    event["body"] = json.dumps(valid_user_data)
    return event


@pytest.fixture
def api_event_with_invalid_user(api_gateway_event, invalid_user_data):
    """
    Complex fixture for testing validation errors
    """
    event = api_gateway_event.copy()
    event["body"] = json.dumps(invalid_user_data)
    return event