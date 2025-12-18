.vscode/settings.json
json{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "terminal.integrated.env.windows": {
        "DOCKER_HOST": "tcp://YOUR_SERVER_IP:PORT"
    },
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
        }
    }
}


src/handlers/hello_handler.py
pythonfrom aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import BaseModel, Field

logger = Logger()
tracer = Tracer()


class RequestBody(BaseModel):
    name: str = Field(..., min_length=1)


class ResponseBody(BaseModel):
    message: str
    name: str


@tracer.capture_lambda_handler
@logger.inject_lambda_context
def handler(event: dict, context: LambdaContext) -> dict:
    body = RequestBody.model_validate_json(event["body"])
    
    response = ResponseBody(
        message=f"Hello, {body.name}!",
        name=body.name
    )
    
    return {
        "statusCode": 200,
        "body": response.model_dump_json()
    }


template.yaml
yamlAWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Runtime: python3.13
    Timeout: 30
    MemorySize: 512
    Environment:
      Variables:
        POWERTOOLS_SERVICE_NAME: my-service
        LOG_LEVEL: INFO

Resources:
  HelloFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: handlers.hello_handler.handler



Run these commands:
powershell# Install dependencies
poetry install

# Deploy to LocalStack
sam build
sam deploy --no-confirm-changeset --resolve-s3
