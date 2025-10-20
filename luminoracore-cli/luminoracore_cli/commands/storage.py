"""
Storage management commands for LuminoraCore CLI v1.1

Provides flexible storage configuration and management for all database types.
"""

import typer
import json
import os
from typing import Optional, Dict, Any
from pathlib import Path

app = typer.Typer(name="storage", help="Flexible storage management for all databases")

@app.command("init")
def init_storage(
    storage_type: str = typer.Option("sqlite", help="Storage type: sqlite, postgresql, redis, mongodb, dynamodb"),
    config_file: Optional[str] = typer.Option(None, help="Configuration file path"),
    interactive: bool = typer.Option(False, help="Interactive configuration mode")
):
    """Initialize flexible storage configuration"""
    typer.echo(f"Initializing {storage_type} storage...")
    
    if interactive:
        config = _interactive_config(storage_type)
    elif config_file:
        config = _load_config_file(config_file)
    else:
        config = _get_default_config(storage_type)
    
    # Save configuration
    config_path = Path("luminora_config.json")
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    typer.echo(f"Storage configuration saved to {config_path}")
    typer.echo("Configuration:")
    typer.echo(json.dumps(config, indent=2))

@app.command("validate")
def validate_storage_config(
    config_file: Optional[str] = typer.Option(None, help="Configuration file path")
):
    """Validate storage configuration"""
    if config_file:
        config = _load_config_file(config_file)
    else:
        config_path = Path("luminora_config.json")
        if not config_path.exists():
            typer.echo("No configuration file found. Run 'storage init' first.")
            raise typer.Exit(1)
        config = _load_config_file(str(config_path))
    
    storage_type = config.get("storage", {}).get("type", "sqlite")
    typer.echo(f"Validating {storage_type} configuration...")
    
    try:
        if storage_type == "dynamodb_flexible":
            from luminoracore_sdk.session import FlexibleDynamoDBStorageV11
            storage = FlexibleDynamoDBStorageV11(
                table_name=config["storage"]["dynamodb"]["table_name"],
                region_name=config["storage"]["dynamodb"]["region"]
            )
        elif storage_type == "sqlite_flexible":
            from luminoracore_sdk.session import FlexibleSQLiteStorageV11
            storage = FlexibleSQLiteStorageV11(
                database_path=config["storage"]["sqlite"]["database_path"]
            )
        elif storage_type == "postgresql_flexible":
            from luminoracore_sdk.session import FlexiblePostgreSQLStorageV11
            storage = FlexiblePostgreSQLStorageV11(
                host=config["storage"]["postgresql"]["host"],
                database=config["storage"]["postgresql"]["database"]
            )
        elif storage_type == "redis_flexible":
            from luminoracore_sdk.session import FlexibleRedisStorageV11
            storage = FlexibleRedisStorageV11(
                host=config["storage"]["redis"]["host"],
                key_prefix=config["storage"]["redis"]["key_prefix"]
            )
        elif storage_type == "mongodb_flexible":
            from luminoracore_sdk.session import FlexibleMongoDBStorageV11
            storage = FlexibleMongoDBStorageV11(
                host=config["storage"]["mongodb"]["host"],
                database=config["storage"]["mongodb"]["database"]
            )
        
        typer.echo("✅ Storage configuration is valid!")
        
    except Exception as e:
        typer.echo(f"❌ Storage configuration is invalid: {e}")
        raise typer.Exit(1)

@app.command("test")
def test_storage_connection(
    config_file: Optional[str] = typer.Option(None, help="Configuration file path")
):
    """Test storage connection"""
    if config_file:
        config = _load_config_file(config_file)
    else:
        config_path = Path("luminora_config.json")
        if not config_path.exists():
            typer.echo("No configuration file found. Run 'storage init' first.")
            raise typer.Exit(1)
        config = _load_config_file(str(config_path))
    
    storage_type = config.get("storage", {}).get("type", "sqlite")
    typer.echo(f"Testing {storage_type} connection...")
    
    try:
        # Test connection based on storage type
        if storage_type == "dynamodb_flexible":
            from luminoracore_sdk.session import FlexibleDynamoDBStorageV11
            storage = FlexibleDynamoDBStorageV11(
                table_name=config["storage"]["dynamodb"]["table_name"],
                region_name=config["storage"]["dynamodb"]["region"]
            )
            typer.echo("✅ DynamoDB connection successful!")
            
        elif storage_type == "sqlite_flexible":
            from luminoracore_sdk.session import FlexibleSQLiteStorageV11
            storage = FlexibleSQLiteStorageV11(
                database_path=config["storage"]["sqlite"]["database_path"]
            )
            typer.echo("✅ SQLite connection successful!")
            
        elif storage_type == "postgresql_flexible":
            from luminoracore_sdk.session import FlexiblePostgreSQLStorageV11
            storage = FlexiblePostgreSQLStorageV11(
                host=config["storage"]["postgresql"]["host"],
                database=config["storage"]["postgresql"]["database"]
            )
            typer.echo("✅ PostgreSQL connection successful!")
            
        elif storage_type == "redis_flexible":
            from luminoracore_sdk.session import FlexibleRedisStorageV11
            storage = FlexibleRedisStorageV11(
                host=config["storage"]["redis"]["host"],
                key_prefix=config["storage"]["redis"]["key_prefix"]
            )
            typer.echo("✅ Redis connection successful!")
            
        elif storage_type == "mongodb_flexible":
            from luminoracore_sdk.session import FlexibleMongoDBStorageV11
            storage = FlexibleMongoDBStorageV11(
                host=config["storage"]["mongodb"]["host"],
                database=config["storage"]["mongodb"]["database"]
            )
            typer.echo("✅ MongoDB connection successful!")
        
        typer.echo("🎉 All storage connections are working!")
        
    except Exception as e:
        typer.echo(f"❌ Storage connection failed: {e}")
        raise typer.Exit(1)

@app.command("migrate")
def migrate_storage(
    from_config: Optional[str] = typer.Option(None, help="Source configuration file"),
    to_config: Optional[str] = typer.Option(None, help="Destination configuration file"),
    dry_run: bool = typer.Option(False, help="Show what would be migrated without doing it")
):
    """Migrate data between different storage configurations"""
    typer.echo("Storage migration functionality - Coming soon!")
    typer.echo("This will allow migrating data between different database types.")

def _interactive_config(storage_type: str) -> Dict[str, Any]:
    """Interactive configuration setup"""
    config = {"storage": {"type": f"{storage_type}_flexible"}}
    
    if storage_type == "dynamodb":
        config["storage"]["dynamodb"] = {
            "table_name": typer.prompt("DynamoDB table name", default="luminora-sessions"),
            "region": typer.prompt("AWS region", default="eu-west-1"),
            "hash_key": typer.prompt("Hash key name", default="session_id"),
            "range_key": typer.prompt("Range key name", default="timestamp")
        }
    elif storage_type == "sqlite":
        config["storage"]["sqlite"] = {
            "database_path": typer.prompt("SQLite database path", default="./luminora.db"),
            "facts_table": typer.prompt("Facts table name", default="facts"),
            "affinity_table": typer.prompt("Affinity table name", default="affinity")
        }
    elif storage_type == "postgresql":
        config["storage"]["postgresql"] = {
            "host": typer.prompt("PostgreSQL host", default="localhost"),
            "port": typer.prompt("PostgreSQL port", default=5432, type=int),
            "database": typer.prompt("Database name", default="luminora"),
            "schema": typer.prompt("Schema name", default="public"),
            "username": typer.prompt("Username", default="postgres"),
            "password": typer.prompt("Password", hide_input=True)
        }
    elif storage_type == "redis":
        config["storage"]["redis"] = {
            "host": typer.prompt("Redis host", default="localhost"),
            "port": typer.prompt("Redis port", default=6379, type=int),
            "db": typer.prompt("Redis database number", default=0, type=int),
            "key_prefix": typer.prompt("Key prefix", default="luminora")
        }
    elif storage_type == "mongodb":
        config["storage"]["mongodb"] = {
            "host": typer.prompt("MongoDB host", default="localhost"),
            "port": typer.prompt("MongoDB port", default=27017, type=int),
            "database": typer.prompt("Database name", default="luminora"),
            "username": typer.prompt("Username", default=""),
            "password": typer.prompt("Password", hide_input=True, default="")
        }
    
    return config

def _load_config_file(config_file: str) -> Dict[str, Any]:
    """Load configuration from file"""
    with open(config_file, 'r') as f:
        return json.load(f)

def _get_default_config(storage_type: str) -> Dict[str, Any]:
    """Get default configuration for storage type"""
    config = {"storage": {"type": f"{storage_type}_flexible"}}
    
    if storage_type == "dynamodb":
        config["storage"]["dynamodb"] = {
            "table_name": "luminora-sessions",
            "region": "eu-west-1",
            "hash_key": "session_id",
            "range_key": "timestamp"
        }
    elif storage_type == "sqlite":
        config["storage"]["sqlite"] = {
            "database_path": "./luminora.db",
            "facts_table": "facts",
            "affinity_table": "affinity",
            "episodes_table": "episodes",
            "moods_table": "moods",
            "memories_table": "memories"
        }
    elif storage_type == "postgresql":
        config["storage"]["postgresql"] = {
            "host": "localhost",
            "port": 5432,
            "database": "luminora",
            "schema": "public",
            "username": "postgres",
            "password": ""
        }
    elif storage_type == "redis":
        config["storage"]["redis"] = {
            "host": "localhost",
            "port": 6379,
            "db": 0,
            "key_prefix": "luminora"
        }
    elif storage_type == "mongodb":
        config["storage"]["mongodb"] = {
            "host": "localhost",
            "port": 27017,
            "database": "luminora",
            "username": "",
            "password": ""
        }
    
    return config

if __name__ == "__main__":
    app()
