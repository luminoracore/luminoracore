# LuminoraCore v1.1 - Serverless Lambda + DynamoDB + DeepSeek Guide

**Complete guide for deploying LuminoraCore in a serverless architecture with AWS Lambda, DynamoDB, and DeepSeek LLM.**

---

## 🏗️ Architecture Overview

```
User Request → API Gateway → Lambda Function → LuminoraCore + DynamoDB → DeepSeek API → Response
```

### Components:
- **AWS Lambda**: Serverless compute for LuminoraCore
- **DynamoDB**: Persistent storage for memory, affinity, and session data
- **DeepSeek API**: LLM provider for AI responses
- **API Gateway**: HTTP endpoints for the application
- **LuminoraCore v1.1**: Memory, affinity, and personality management

---

## 🔧 Key Considerations for Serverless Deployment

### 1. **Lambda Function Configuration**

#### Memory & Timeout Settings
```yaml
# serverless.yml or AWS Console
functions:
  luminora-core:
    memorySize: 1024  # Minimum for LuminoraCore
    timeout: 30       # Seconds - DeepSeek can take time
    runtime: python3.11
```

#### Environment Variables
```yaml
environment:
  DEEPSEEK_API_KEY: ${env:DEEPSEEK_API_KEY}
  DYNAMODB_TABLE_NAME: luminora-sessions
  AWS_REGION: us-east-1
  LUMINORA_STORAGE_TYPE: dynamodb
  LUMINORA_DEMO_MODE: false
```

### 2. **DynamoDB Table Design**

#### Main Sessions Table
```json
{
  "TableName": "luminora-sessions",
  "KeySchema": [
    {
      "AttributeName": "PK",
      "KeyType": "HASH"
    },
    {
      "AttributeName": "SK",
      "KeyType": "RANGE"
    }
  ],
  "AttributeDefinitions": [
    {
      "AttributeName": "PK",
      "AttributeType": "S"
    },
    {
      "AttributeName": "SK",
      "AttributeType": "S"
    }
  ],
  "BillingMode": "PAY_PER_REQUEST"
}
```

#### Data Structure
```json
{
  "PK": "USER#user123",
  "SK": "SESSION#session456",
  "GSI1PK": "PERSONALITY#Assistant",
  "GSI1SK": "USER#user123",
  "session_id": "session456",
  "user_id": "user123",
  "personality_name": "Assistant",
  "created_at": "2025-10-18T21:00:00Z",
  "last_activity": "2025-10-18T21:30:00Z",
  "affinity_data": {
    "current_level": "friend",
    "affinity_points": 45,
    "total_interactions": 12,
    "positive_interactions": 10,
    "negative_interactions": 1
  },
  "facts": [
    {
      "fact": "hobby",
      "value": "photography",
      "confidence": 0.9,
      "created_at": "2025-10-18T21:15:00Z"
    }
  ],
  "episodes": [
    {
      "episode_type": "achievement",
      "description": "User completed photography course",
      "importance": 0.8,
      "created_at": "2025-10-18T21:20:00Z"
    }
  ],
  "mood_history": [
    {
      "mood": "positive",
      "intensity": 0.7,
      "created_at": "2025-10-18T21:25:00Z"
    }
  ]
}
```

### 3. **Lambda Function Code Structure**

#### Main Handler
```python
import json
import asyncio
from luminoracore_sdk import LuminoraCoreClientV11, DynamoDBStorageV11

# Initialize storage (outside handler for reuse)
storage = DynamoDBStorageV11(
    region_name="us-east-1",
    table_name="luminora-sessions"
)

async def process_message(user_id, session_id, message, personality_name="Assistant"):
    """Process user message with LuminoraCore"""
    client = LuminoraCoreClientV11(
        storage=storage,
        personality_name=personality_name,
        llm_provider="deepseek",
        llm_api_key=os.environ["DEEPSEEK_API_KEY"]
    )
    
    # Process message with memory and affinity
    response = await client.process_message(session_id, message)
    
    # Get updated affinity
    affinity = await client.get_affinity(user_id, personality_name)
    
    return {
        "response": response,
        "affinity_level": affinity.get("current_level", "stranger"),
        "affinity_points": affinity.get("affinity_points", 0)
    }

def lambda_handler(event, context):
    """AWS Lambda handler"""
    try:
        # Parse request
        body = json.loads(event["body"])
        user_id = body["user_id"]
        session_id = body["session_id"]
        message = body["message"]
        personality_name = body.get("personality_name", "Assistant")
        
        # Process message
        result = asyncio.run(process_message(user_id, session_id, message, personality_name))
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(result)
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
```

### 4. **DeepSeek Integration**

#### Configuration
```python
# In your Lambda function
import os
from luminoracore_sdk import LuminoraCoreClientV11

# Configure DeepSeek
client = LuminoraCoreClientV11(
    storage=storage,
    personality_name="Assistant",
    llm_provider="deepseek",
    llm_api_key=os.environ["DEEPSEEK_API_KEY"],
    llm_model="deepseek-chat",
    llm_base_url="https://api.deepseek.com/v1"
)
```

#### DeepSeek API Considerations
```python
# Rate limiting and error handling
async def call_deepseek_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = await client._call_llm(prompt)
            return response
        except Exception as e:
            if "rate_limit" in str(e).lower():
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise e
    raise Exception("Max retries exceeded")
```

---

## 🚀 Deployment Considerations

### 1. **Lambda Layer for Dependencies**

#### Create Layer
```bash
# Create deployment package
mkdir python
pip install luminoracore-sdk-python -t python/
pip install boto3 -t python/
pip install requests -t python/

# Create layer
zip -r luminora-layer.zip python/
```

#### Use Layer in Lambda
```yaml
# serverless.yml
functions:
  luminora-core:
    layers:
      - arn:aws:lambda:us-east-1:123456789012:layer:luminora-layer:1
```

### 2. **Cold Start Optimization**

#### Connection Reuse
```python
# Global variables (reused across invocations)
storage = None
client = None

def get_storage():
    global storage
    if storage is None:
        storage = DynamoDBStorageV11(
            region_name="us-east-1",
            table_name="luminora-sessions"
        )
    return storage

def get_client():
    global client
    if client is None:
        client = LuminoraCoreClientV11(
            storage=get_storage(),
            personality_name="Assistant"
        )
    return client
```

#### Provisioned Concurrency (Optional)
```yaml
# For production with consistent traffic
provisionedConcurrency: 5
```

### 3. **DynamoDB Performance**

#### Read/Write Capacity
```yaml
# For predictable workloads
DynamoDBTable:
  Type: AWS::DynamoDB::Table
  Properties:
    BillingMode: PROVISIONED
    ProvisionedThroughput:
      ReadCapacityUnits: 5
      WriteCapacityUnits: 5
```

#### Global Secondary Indexes
```json
{
  "GlobalSecondaryIndexes": [
    {
      "IndexName": "GSI1",
      "KeySchema": [
        {
          "AttributeName": "GSI1PK",
          "KeyType": "HASH"
        },
        {
          "AttributeName": "GSI1SK",
          "KeyType": "RANGE"
        }
      ],
      "Projection": {
        "ProjectionType": "ALL"
      }
    }
  ]
}
```

---

## 🔒 Security Considerations

### 1. **API Security**
```python
# API Gateway with API Key
def lambda_handler(event, context):
    # Check API key
    api_key = event.get("headers", {}).get("x-api-key")
    if api_key != os.environ["API_KEY"]:
        return {"statusCode": 401, "body": "Unauthorized"}
    
    # Continue processing...
```

### 2. **Environment Variables**
```yaml
# Use AWS Systems Manager Parameter Store
environment:
  DEEPSEEK_API_KEY: ${ssm:/luminora/deepseek-api-key}
  API_KEY: ${ssm:/luminora/api-key}
```

### 3. **IAM Permissions**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:Query",
        "dynamodb:Scan"
      ],
      "Resource": "arn:aws:dynamodb:us-east-1:123456789012:table/luminora-sessions"
    }
  ]
}
```

---

## 📊 Monitoring & Logging

### 1. **CloudWatch Logs**
```python
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Processing request: {event}")
    
    try:
        result = asyncio.run(process_message(...))
        logger.info(f"Success: {result}")
        return result
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise
```

### 2. **CloudWatch Metrics**
```python
# Custom metrics
import boto3

cloudwatch = boto3.client('cloudwatch')

def send_metric(metric_name, value, unit='Count'):
    cloudwatch.put_metric_data(
        Namespace='LuminoraCore',
        MetricData=[
            {
                'MetricName': metric_name,
                'Value': value,
                'Unit': unit
            }
        ]
    )

# Usage
send_metric('MessagesProcessed', 1)
send_metric('AffinityLevel', affinity_points, 'None')
```

---

## 🧪 Testing Strategy

### 1. **Local Testing**
```python
# test_lambda.py
import asyncio
from lambda_function import process_message

async def test_message_processing():
    result = await process_message(
        user_id="test_user",
        session_id="test_session",
        message="Hello, I'm testing the system"
    )
    assert result["response"] is not None
    assert "affinity_level" in result

if __name__ == "__main__":
    asyncio.run(test_message_processing())
```

### 2. **Integration Testing**
```python
# Test with DynamoDB Local
import boto3
from moto import mock_dynamodb

@mock_dynamodb
def test_dynamodb_integration():
    # Create mock table
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.create_table(
        TableName='test-table',
        KeySchema=[
            {'AttributeName': 'PK', 'KeyType': 'HASH'},
            {'AttributeName': 'SK', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'PK', 'AttributeType': 'S'},
            {'AttributeName': 'SK', 'AttributeType': 'S'}
        ]
    )
    
    # Test storage
    storage = DynamoDBStorageV11(
        region_name="us-east-1",
        table_name="test-table"
    )
    
    # Test operations...
```

---

## 💰 Cost Optimization

### 1. **Lambda Costs**
- **Memory**: Start with 1024MB, adjust based on performance
- **Timeout**: Set to 30 seconds max
- **Provisioned Concurrency**: Only for consistent traffic

### 2. **DynamoDB Costs**
- **On-Demand**: For unpredictable workloads
- **Provisioned**: For predictable workloads
- **TTL**: Set TTL on old sessions to reduce storage costs

### 3. **DeepSeek API Costs**
- **Model Selection**: Use `deepseek-chat` (cheaper than `deepseek-coder`)
- **Prompt Optimization**: Minimize prompt length
- **Caching**: Cache responses for similar queries

---

## 🚀 Complete Serverless Template

### serverless.yml
```yaml
service: luminora-core-serverless

provider:
  name: aws
  runtime: python3.11
  region: us-east-1
  memorySize: 1024
  timeout: 30
  environment:
    DEEPSEEK_API_KEY: ${ssm:/luminora/deepseek-api-key}
    DYNAMODB_TABLE_NAME: ${self:service}-sessions-${self:provider.stage}
  iam:
    role:
      statements:
        - Effect: Allow
          Action:
            - dynamodb:*
          Resource:
            - arn:aws:dynamodb:${self:provider.region}:*:table/${self:service}-sessions-${self:provider.stage}
            - arn:aws:dynamodb:${self:provider.region}:*:table/${self:service}-sessions-${self:provider.stage}/index/*

functions:
  processMessage:
    handler: lambda_function.lambda_handler
    events:
      - http:
          path: /message
          method: post
          cors: true
    layers:
      - arn:aws:lambda:${self:provider.region}:123456789012:layer:luminora-layer:1

resources:
  Resources:
    SessionsTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: ${self:service}-sessions-${self:provider.stage}
        BillingMode: PAY_PER_REQUEST
        AttributeDefinitions:
          - AttributeName: PK
            AttributeType: S
          - AttributeName: SK
            AttributeType: S
        KeySchema:
          - AttributeName: PK
            KeyType: HASH
          - AttributeName: SK
            KeyType: RANGE
        TimeToLiveSpecification:
          AttributeName: ttl
          Enabled: true
```

### Deployment Commands
```bash
# Deploy
serverless deploy

# Test locally
serverless invoke local -f processMessage -d '{"user_id":"test","session_id":"test","message":"Hello"}'

# Monitor logs
serverless logs -f processMessage --tail
```

---

## 🎯 Best Practices Summary

1. **Start Simple**: Begin with basic Lambda + DynamoDB setup
2. **Optimize Cold Starts**: Use global variables and layers
3. **Monitor Costs**: Set up CloudWatch billing alerts
4. **Handle Errors**: Implement proper error handling and retries
5. **Security First**: Use IAM roles and API keys
6. **Test Thoroughly**: Test locally and with mock services
7. **Scale Gradually**: Start with on-demand, move to provisioned as needed

---

**Ready to deploy LuminoraCore in a serverless architecture! 🚀**
