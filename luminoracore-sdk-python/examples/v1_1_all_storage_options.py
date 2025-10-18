"""
Complete v1.1 All Storage Options Example

Demonstrates all available storage implementations:
- SQLite (local file)
- PostgreSQL (relational)
- MySQL (relational)
- MongoDB (document)
- Redis (key-value)
- DynamoDB (cloud NoSQL)
"""

import asyncio
import json
from datetime import datetime
from luminoracore_sdk import (
    LuminoraCoreClient,
    LuminoraCoreClientV11,
    SQLiteStorageV11,
    PostgreSQLStorageV11,
    MySQLStorageV11,
    MongoDBStorageV11,
    RedisStorageV11,
    DynamoDBStorageV11
)


async def demo_storage(storage_name: str, storage_instance, client_v11):
    """Demo a specific storage implementation"""
    print(f"\n🗄️  {storage_name} Storage Demo")
    print("-" * 50)
    
    user_id = f"demo_user_{storage_name.lower()}"
    
    try:
        # Test basic operations
        print(f"✅ Testing {storage_name} storage...")
        
        # Save facts
        await client_v11.save_fact(user_id, "preferences", "language", "Python", confidence=0.9)
        await client_v11.save_fact(user_id, "preferences", "framework", "FastAPI", confidence=0.8)
        await client_v11.save_fact(user_id, "personal_info", "name", "Demo User", confidence=0.95)
        
        # Save episodes
        await client_v11.save_episode(
            user_id, "milestone", "First success", 
            f"Successfully tested {storage_name} storage", 8.5, "positive"
        )
        
        # Retrieve data
        facts = await client_v11.get_facts(user_id)
        episodes = await client_v11.get_episodes(user_id, min_importance=8.0)
        
        print(f"   📊 Saved {len(facts)} facts and {len(episodes)} episodes")
        print(f"   📈 Facts: {[f'{f['category']}:{f['key']}' for f in facts]}")
        print(f"   📈 Episodes: {[f'{e['type']}:{e['title']}' for e in episodes]}")
        
        # Test sentiment analysis
        sentiment_result = await client_v11.analyze_sentiment(
            user_id, f"I'm really happy with the {storage_name} integration!"
        )
        print(f"   🧠 Sentiment: {sentiment_result['sentiment']} (confidence: {sentiment_result.get('confidence', 0):.2f})")
        
        # Test personality evolution
        session_id = f"{user_id}_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        evolution_result = await client_v11.evolve_personality(session_id, user_id)
        print(f"   🔄 Evolution: {'Changes detected' if evolution_result['changes_detected'] else 'No changes'}")
        
        # Test session export
        snapshot = await client_v11.export_snapshot(session_id)
        print(f"   📦 Export: {snapshot['_snapshot_info']['total_messages']} messages exported")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error with {storage_name}: {e}")
        return False


async def main():
    """Complete storage options demonstration"""
    
    print("🚀 LuminoraCore v1.1 - All Storage Options Demo")
    print("=" * 80)
    
    # Initialize base client
    client = LuminoraCoreClient()
    await client.initialize()
    
    # ========================================
    # 1. SQLITE STORAGE
    # ========================================
    sqlite_storage = SQLiteStorageV11("demo_all_storage.db")
    client_v11_sqlite = LuminoraCoreClientV11(client, storage_v11=sqlite_storage)
    
    await demo_storage("SQLite", sqlite_storage, client_v11_sqlite)
    
    # ========================================
    # 2. POSTGRESQL STORAGE (Optional)
    # ========================================
    try:
        # Note: Requires PostgreSQL server running
        postgresql_storage = PostgreSQLStorageV11(
            "postgresql://user:password@localhost:5432/luminoracore_v11"
        )
        client_v11_postgresql = LuminoraCoreClientV11(client, storage_v11=postgresql_storage)
        
        await demo_storage("PostgreSQL", postgresql_storage, client_v11_postgresql)
        
    except Exception as e:
        print(f"\n🗄️  PostgreSQL Storage Demo")
        print("-" * 50)
        print(f"   ⚠️  PostgreSQL not available: {e}")
        print(f"   ℹ️  To use: Install PostgreSQL and asyncpg: pip install asyncpg")
        print(f"   ℹ️  Configure connection string in the code above")
    
    # ========================================
    # 3. MYSQL STORAGE (Optional)
    # ========================================
    try:
        # Note: Requires MySQL server running
        mysql_storage = MySQLStorageV11(
            host="localhost",
            port=3306,
            user="root",
            password="password",
            database="luminoracore_v11"
        )
        client_v11_mysql = LuminoraCoreClientV11(client, storage_v11=mysql_storage)
        
        await demo_storage("MySQL", mysql_storage, client_v11_mysql)
        
    except Exception as e:
        print(f"\n🗄️  MySQL Storage Demo")
        print("-" * 50)
        print(f"   ⚠️  MySQL not available: {e}")
        print(f"   ℹ️  To use: Install MySQL and aiomysql: pip install aiomysql")
        print(f"   ℹ️  Configure connection parameters in the code above")
    
    # ========================================
    # 4. MONGODB STORAGE (Optional)
    # ========================================
    try:
        # Note: Requires MongoDB server running
        mongodb_storage = MongoDBStorageV11(
            "mongodb://localhost:27017",
            "luminoracore_v11"
        )
        client_v11_mongodb = LuminoraCoreClientV11(client, storage_v11=mongodb_storage)
        
        await demo_storage("MongoDB", mongodb_storage, client_v11_mongodb)
        
    except Exception as e:
        print(f"\n🗄️  MongoDB Storage Demo")
        print("-" * 50)
        print(f"   ⚠️  MongoDB not available: {e}")
        print(f"   ℹ️  To use: Install MongoDB and motor: pip install motor")
        print(f"   ℹ️  Configure connection string in the code above")
    
    # ========================================
    # 5. REDIS STORAGE (Optional)
    # ========================================
    try:
        # Note: Requires Redis server running
        redis_storage = RedisStorageV11(
            host="localhost",
            port=6379,
            db=0
        )
        client_v11_redis = LuminoraCoreClientV11(client, storage_v11=redis_storage)
        
        await demo_storage("Redis", redis_storage, client_v11_redis)
        
    except Exception as e:
        print(f"\n🗄️  Redis Storage Demo")
        print("-" * 50)
        print(f"   ⚠️  Redis not available: {e}")
        print(f"   ℹ️  To use: Install Redis and redis: pip install redis")
        print(f"   ℹ️  Start Redis server: redis-server")
    
    # ========================================
    # 6. DYNAMODB STORAGE (Optional)
    # ========================================
    try:
        # Note: Requires AWS credentials configured
        dynamodb_storage = DynamoDBStorageV11(
            table_name="luminoracore-v11-demo",
            region_name="us-east-1"
        )
        client_v11_dynamodb = LuminoraCoreClientV11(client, storage_v11=dynamodb_storage)
        
        await demo_storage("DynamoDB", dynamodb_storage, client_v11_dynamodb)
        
    except Exception as e:
        print(f"\n🗄️  DynamoDB Storage Demo")
        print("-" * 50)
        print(f"   ⚠️  DynamoDB not available: {e}")
        print(f"   ℹ️  To use: Configure AWS credentials and boto3: pip install boto3")
        print(f"   ℹ️  Set up AWS credentials: aws configure")
    
    # ========================================
    # 7. STORAGE COMPARISON
    # ========================================
    print(f"\n📊 Storage Options Summary")
    print("=" * 80)
    
    storage_options = [
        ("SQLite", "✅ Always available", "Local file", "Perfect for development"),
        ("PostgreSQL", "⚠️  Requires server", "Relational", "Enterprise production"),
        ("MySQL", "⚠️  Requires server", "Relational", "Web applications"),
        ("MongoDB", "⚠️  Requires server", "Document", "Flexible schemas"),
        ("Redis", "⚠️  Requires server", "Key-Value", "High performance caching"),
        ("DynamoDB", "⚠️  Requires AWS", "Cloud NoSQL", "Serverless applications")
    ]
    
    for name, availability, type_desc, use_case in storage_options:
        print(f"   {name:12} | {availability:18} | {type_desc:12} | {use_case}")
    
    # ========================================
    # 8. RECOMMENDATIONS
    # ========================================
    print(f"\n🎯 Storage Recommendations")
    print("-" * 50)
    
    print("   🚀 Development:")
    print("      → SQLite (no setup required)")
    
    print("   🏢 Production (Small-Medium):")
    print("      → PostgreSQL (robust, ACID compliance)")
    print("      → MySQL (popular, well-supported)")
    
    print("   ☁️  Production (Cloud/Serverless):")
    print("      → DynamoDB (AWS managed, scales automatically)")
    print("      → MongoDB Atlas (cloud managed)")
    
    print("   ⚡ High Performance:")
    print("      → Redis (caching, session storage)")
    print("      → PostgreSQL + Redis (hybrid approach)")
    
    print("   🔄 Hybrid Approach:")
    print("      → SQLite for development")
    print("      → PostgreSQL for production")
    print("      → Redis for caching")
    
    print(f"\n✅ All storage implementations are complete and production-ready!")
    print(f"   Choose based on your specific requirements and infrastructure.")
    
    await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
