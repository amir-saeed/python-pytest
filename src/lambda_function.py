import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import BaseModel, ValidationError

logger = Logger()


class User(BaseModel):
    """User model with validation"""
    name: str
    email: str
    age: int


def lambda_handler(event: dict, context: LambdaContext) -> dict:
    """
    Lambda handler to create a user
    """
    try:
        # Parse body
        body = json.loads(event.get("body", "{}"))
        
        # Validate with Pydantic
        user = User(**body)
        
        logger.info("User created", extra={"user": user.model_dump()})
        
        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "User created successfully",
                "user": user.model_dump()
            })
        }
        
    except ValidationError as e:
        logger.error("Validation error", extra={"error": str(e)})
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid input", "details": e.errors()})
        }
        
    except Exception as e:
        logger.error("Unexpected error", extra={"error": str(e)})
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"})
        }