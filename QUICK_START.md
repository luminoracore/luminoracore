# LuminoraCore v1.1 Quick Start

Get up and running with LuminoraCore in 5 minutes.

## Installation

```bash
# Install all components
pip install -e luminoracore/
pip install -e luminoracore-sdk-python/
pip install -e luminoracore-cli/
```

## Your First Intelligent Bot

```python
import asyncio
from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11

async def main():
    # Initialize client
    base_client = LuminoraCoreClient()
    await base_client.initialize()
    
    # Setup storage
    storage = InMemoryStorageV11()
    client = LuminoraCoreClientV11(base_client, storage_v11=storage)
    
    # Create session
    session_id = await client.create_session(
        personality_name="helpful_assistant",
        provider_config={"name": "openai", "model": "gpt-3.5-turbo"}
    )
    
    # Save user information
    await client.save_fact(
        user_id=session_id,
        category="personal_info",
        key="name",
        value="Carlos",
        confidence=0.95
    )
    
    # Send message with memory
    response = await client.send_message_with_memory(
        session_id=session_id,
        user_message="Hello, what do you remember about me?",
        personality_name="helpful_assistant",
        provider_config={"name": "openai", "model": "gpt-3.5-turbo"}
    )
    
    print(f"Response: {response['response']}")
    print(f"Context used: {response['context_used']}")
    
    await base_client.cleanup()

# Run the example
asyncio.run(main())
```

## CLI Quick Start

```bash
# Check version
luminoracore --version

# Initialize storage
luminoracore storage init

# View memory
luminoracore memory list

# Run validation
luminoracore validate personalities/
```

## Storage Setup

### SQLite (Simplest)

```python
from luminoracore_sdk import FlexibleSQLiteStorageV11

storage = FlexibleSQLiteStorageV11("luminora.db")
```

### DynamoDB (Production)

```python
from luminoracore_sdk import FlexibleDynamoDBStorageV11

storage = FlexibleDynamoDBStorageV11(
    table_name="luminora-table",
    region_name="us-east-1"
)
```

## Complete Example

Run the complete demo:

```bash
python examples/luminoracore_v1_1_complete_demo.py
```

This example demonstrates:
- Memory management
- Fact extraction
- Affinity tracking
- Personality evolution
- Context-aware conversations

## Next Steps

1. **Read Documentation**: Check component docs
2. **Configure Storage**: Set up your database
3. **Create Personalities**: Build custom AI personalities
4. **Integrate**: Use in your application

## Need Help?

- **Documentation**: Check docs/ directories
- **Examples**: See examples/ directory
- **Issues**: GitHub Issues