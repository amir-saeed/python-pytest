import json
import pytest
from src.lambda_function import lambda_handler


def test_create_user_success(api_event_with_valid_user, lambda_context):
    """Test successful user creation"""
    # Act
    response = lambda_handler(api_event_with_valid_user, lambda_context)
    
    # Assert
    assert response["statusCode"] == 201
    
    body = json.loads(response["body"])
    assert body["message"] == "User created successfully"
    assert body["user"]["name"] == "John Doe"
    assert body["user"]["email"] == "john@example.com"
    assert body["user"]["age"] == 30


def test_create_user_validation_error(api_event_with_invalid_user, lambda_context):
    """Test validation error when email is missing"""
    # Act
    response = lambda_handler(api_event_with_invalid_user, lambda_context)
    
    # Assert
    assert response["statusCode"] == 400
    
    body = json.loads(response["body"])
    assert body["error"] == "Invalid input"
    assert "details" in body


def test_create_user_malformed_json(api_gateway_event, lambda_context):
    """Test with malformed JSON"""
    # Arrange
    api_gateway_event["body"] = "not valid json{"
    
    # Act
    response = lambda_handler(api_gateway_event, lambda_context)
    
    # Assert
    assert response["statusCode"] == 500


def test_create_user_empty_body(api_gateway_event, lambda_context):
    """Test with empty body"""
    # Arrange
    api_gateway_event["body"] = "{}"
    
    # Act
    response = lambda_handler(api_gateway_event, lambda_context)
    
    # Assert
    assert response["statusCode"] == 400