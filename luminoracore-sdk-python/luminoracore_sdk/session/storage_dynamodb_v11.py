"""
DynamoDB Storage v1.1 Implementation

Real DynamoDB implementation for v1.1 storage with persistent data.
"""

import json
import boto3
from botocore.exceptions import ClientError
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from .storage_v1_1 import StorageV11Extension

logger = logging.getLogger(__name__)


class DynamoDBStorageV11(StorageV11Extension):
    """
    Real DynamoDB storage implementation for v1.1 features
    """
    
    def __init__(self, table_name: str = "luminoracore-v11", region_name: str = "us-east-1"):
        """
        Initialize DynamoDB storage
        
        Args:
            table_name: DynamoDB table name
            region_name: AWS region name
        """
        self.table_name = table_name
        self.region_name = region_name
        
        try:
            self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
            self.table = self.dynamodb.Table(table_name)
            self._ensure_table_exists()
            logger.info(f"DynamoDB storage initialized with table: {table_name}")
        except Exception as e:
            logger.error(f"Failed to initialize DynamoDB storage: {e}")
            raise
    
    def _ensure_table_exists(self):
        """Ensure DynamoDB table exists with proper schema"""
        try:
            # Try to describe table to check if it exists
            self.table.table_status
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                logger.info(f"Creating DynamoDB table: {self.table_name}")
                self._create_table()
            else:
                raise
    
    def _create_table(self):
        """Create DynamoDB table with proper schema"""
        try:
            self.dynamodb.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {
                        'AttributeName': 'PK',
                        'KeyType': 'HASH'  # Partition key
                    },
                    {
                        'AttributeName': 'SK',
                        'KeyType': 'RANGE'  # Sort key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'PK',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'SK',
                        'AttributeType': 'S'
                    }
                ],
                BillingMode='PAY_PER_REQUEST'
            )
            
            # Wait for table to be created
            waiter = self.dynamodb.meta.client.get_waiter('table_exists')
            waiter.wait(TableName=self.table_name)
            logger.info(f"DynamoDB table {self.table_name} created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create DynamoDB table: {e}")
            raise
    
    def _get_affinity_pk(self, user_id: str, personality_name: str) -> str:
        """Get partition key for affinity data"""
        return f"AFFINITY#{user_id}#{personality_name}"
    
    def _get_fact_pk(self, user_id: str, category: str, key: str) -> str:
        """Get partition key for fact data"""
        return f"FACT#{user_id}#{category}#{key}"
    
    def _get_episode_pk(self, user_id: str, episode_id: str) -> str:
        """Get partition key for episode data"""
        return f"EPISODE#{user_id}#{episode_id}"
    
    def _get_mood_pk(self, user_id: str, session_id: str) -> str:
        """Get partition key for mood data"""
        return f"MOOD#{user_id}#{session_id}"
    
    def _get_memory_pk(self, session_id: str, memory_key: str) -> str:
        """Get partition key for memory data"""
        return f"MEMORY#{session_id}#{memory_key}"
    
    # AFFINITY METHODS
    async def save_affinity(
        self,
        user_id: str,
        personality_name: str,
        affinity_points: int,
        current_level: str,
        **kwargs
    ) -> bool:
        """Save or update user affinity"""
        try:
            pk = self._get_affinity_pk(user_id, personality_name)
            
            item = {
                'PK': pk,
                'SK': 'AFFINITY',
                'GSI1PK': f"USER#{user_id}",
                'GSI1SK': f"PERSONALITY#{personality_name}",
                'affinity_points': affinity_points,
                'current_level': current_level,
                'total_interactions': kwargs.get('total_interactions', 0),
                'positive_interactions': kwargs.get('positive_interactions', 0),
                'created_at': kwargs.get('created_at', datetime.now().isoformat()),
                'updated_at': datetime.now().isoformat(),
                'TTL': int((datetime.now() + timedelta(days=365)).timestamp())
            }
            
            self.table.put_item(Item=item)
            return True
            
        except Exception as e:
            logger.error(f"Failed to save affinity: {e}")
            return False
    
    async def get_affinity(
        self,
        user_id: str,
        personality_name: str
    ) -> Optional[Dict[str, Any]]:
        """Get user affinity data"""
        try:
            pk = self._get_affinity_pk(user_id, personality_name)
            
            response = self.table.get_item(
                Key={
                    'PK': pk,
                    'SK': 'AFFINITY'
                }
            )
            
            if 'Item' in response:
                item = response['Item']
                return {
                    "affinity_points": item.get('affinity_points', 0),
                    "current_level": item.get('current_level', 'stranger'),
                    "total_interactions": item.get('total_interactions', 0),
                    "positive_interactions": item.get('positive_interactions', 0),
                    "created_at": item.get('created_at'),
                    "updated_at": item.get('updated_at')
                }
            return None
            
        except Exception as e:
            logger.error(f"Failed to get affinity: {e}")
            return None
    
    # FACT METHODS
    async def save_fact(
        self,
        user_id: str,
        category: str,
        key: str,
        value: Any,
        **kwargs
    ) -> bool:
        """Save a user fact"""
        try:
            pk = self._get_fact_pk(user_id, category, key)
            
            item = {
                'PK': pk,
                'SK': 'FACT',
                'GSI1PK': f"USER#{user_id}",
                'GSI1SK': f"CATEGORY#{category}",
                'category': category,
                'key': key,
                'value': json.dumps(value) if not isinstance(value, str) else value,
                'confidence': kwargs.get('confidence', 1.0),
                'created_at': kwargs.get('created_at', datetime.now().isoformat()),
                'updated_at': datetime.now().isoformat(),
                'TTL': int((datetime.now() + timedelta(days=365)).timestamp())
            }
            
            self.table.put_item(Item=item)
            return True
            
        except Exception as e:
            logger.error(f"Failed to save fact: {e}")
            return False
    
    async def get_facts(
        self,
        user_id: str,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get user facts, optionally filtered by category"""
        try:
            if category:
                # Query by category
                response = self.table.query(
                    IndexName='GSI1',
                    KeyConditionExpression='GSI1PK = :user_id AND begins_with(GSI1SK, :category)',
                    ExpressionAttributeValues={
                        ':user_id': f"USER#{user_id}",
                        ':category': f"CATEGORY#{category}"
                    }
                )
            else:
                # Query all facts for user
                response = self.table.query(
                    IndexName='GSI1',
                    KeyConditionExpression='GSI1PK = :user_id',
                    ExpressionAttributeValues={
                        ':user_id': f"USER#{user_id}"
                    }
                )
            
            facts = []
            for item in response.get('Items', []):
                try:
                    value = json.loads(item['value']) if item['value'].startswith(('{', '[', '"')) else item['value']
                except:
                    value = item['value']
                
                facts.append({
                    "category": item['category'],
                    "key": item['key'],
                    "value": value,
                    "confidence": item.get('confidence', 1.0),
                    "created_at": item.get('created_at'),
                    "updated_at": item.get('updated_at')
                })
            
            return facts
            
        except Exception as e:
            logger.error(f"Failed to get facts: {e}")
            return []
    
    # EPISODE METHODS
    async def save_episode(
        self,
        user_id: str,
        episode_type: str,
        title: str,
        summary: str,
        importance: float,
        sentiment: str,
        **kwargs
    ) -> bool:
        """Save an episode"""
        try:
            episode_id = kwargs.get('episode_id', datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
            pk = self._get_episode_pk(user_id, episode_id)
            
            item = {
                'PK': pk,
                'SK': 'EPISODE',
                'GSI1PK': f"USER#{user_id}",
                'GSI1SK': f"TYPE#{episode_type}#{episode_id}",
                'episode_type': episode_type,
                'title': title,
                'summary': summary,
                'importance': importance,
                'sentiment': sentiment,
                'created_at': datetime.now().isoformat(),
                'TTL': int((datetime.now() + timedelta(days=365)).timestamp())
            }
            
            self.table.put_item(Item=item)
            return True
            
        except Exception as e:
            logger.error(f"Failed to save episode: {e}")
            return False
    
    async def get_episodes(
        self,
        user_id: str,
        min_importance: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Get episodes, optionally filtered by importance"""
        try:
            response = self.table.query(
                IndexName='GSI1',
                KeyConditionExpression='GSI1PK = :user_id',
                ExpressionAttributeValues={
                    ':user_id': f"USER#{user_id}"
                }
            )
            
            episodes = []
            for item in response.get('Items', []):
                if min_importance is not None and item.get('importance', 0) < min_importance:
                    continue
                
                episodes.append({
                    "episode_type": item['episode_type'],
                    "title": item['title'],
                    "summary": item['summary'],
                    "importance": item.get('importance', 0),
                    "sentiment": item.get('sentiment', 'neutral'),
                    "created_at": item.get('created_at')
                })
            
            # Sort by importance descending
            episodes.sort(key=lambda x: x['importance'], reverse=True)
            return episodes
            
        except Exception as e:
            logger.error(f"Failed to get episodes: {e}")
            return []
    
    # MOOD METHODS
    async def save_mood(
        self,
        session_id: str,
        user_id: str,
        current_mood: str,
        mood_intensity: float = 1.0
    ) -> bool:
        """Save current mood state"""
        try:
            pk = self._get_mood_pk(user_id, session_id)
            
            item = {
                'PK': pk,
                'SK': 'MOOD',
                'GSI1PK': f"USER#{user_id}",
                'GSI1SK': f"SESSION#{session_id}",
                'current_mood': current_mood,
                'mood_intensity': mood_intensity,
                'created_at': datetime.now().isoformat(),
                'TTL': int((datetime.now() + timedelta(days=30)).timestamp())
            }
            
            self.table.put_item(Item=item)
            return True
            
        except Exception as e:
            logger.error(f"Failed to save mood: {e}")
            return False
    
    async def get_mood_history(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get mood history for user"""
        try:
            response = self.table.query(
                IndexName='GSI1',
                KeyConditionExpression='GSI1PK = :user_id',
                ExpressionAttributeValues={
                    ':user_id': f"USER#{user_id}"
                },
                Limit=limit
            )
            
            moods = []
            for item in response.get('Items', []):
                if item.get('SK') == 'MOOD':
                    moods.append({
                        "session_id": item['GSI1SK'].replace('SESSION#', ''),
                        "current_mood": item['current_mood'],
                        "mood_intensity": item.get('mood_intensity', 1.0),
                        "created_at": item.get('created_at')
                    })
            
            return moods
            
        except Exception as e:
            logger.error(f"Failed to get mood history: {e}")
            return []
    
    async def get_mood(
        self,
        session_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get current mood state"""
        try:
            response = self.table.query(
                IndexName='SessionIndex',
                KeyConditionExpression=Key('session_id').eq(session_id),
                ScanIndexForward=False,
                Limit=1
            )
            
            items = response.get('Items', [])
            if items:
                item = items[0]
                return {
                    "current_mood": item.get('current_mood'),
                    "mood_intensity": item.get('mood_intensity', 1.0),
                    "created_at": item.get('created_at')
                }
            return None
            
        except Exception as e:
            logger.error(f"Failed to get mood: {e}")
            return None
    
    # MEMORY METHODS
    async def save_memory(
        self,
        session_id: str,
        user_id: str,
        key: str,
        value: Any,
        expires_at: Optional[datetime] = None
    ) -> bool:
        """Save conversation memory"""
        try:
            pk = self._get_memory_pk(session_id, key)
            
            item = {
                'PK': pk,
                'SK': 'MEMORY',
                'GSI1PK': f"SESSION#{session_id}",
                'GSI1SK': f"KEY#{key}",
                'memory_key': key,
                'memory_value': json.dumps(value) if not isinstance(value, str) else value,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            if expires_at:
                item['TTL'] = int(expires_at.timestamp())
            else:
                # Default TTL of 30 days
                item['TTL'] = int((datetime.now() + timedelta(days=30)).timestamp())
            
            self.table.put_item(Item=item)
            return True
            
        except Exception as e:
            logger.error(f"Failed to save memory: {e}")
            return False
    
    async def get_memory(
        self,
        session_id: str,
        key: str
    ) -> Optional[Any]:
        """Get conversation memory"""
        try:
            pk = self._get_memory_pk(session_id, key)
            
            response = self.table.get_item(
                Key={
                    'PK': pk,
                    'SK': 'MEMORY'
                }
            )
            
            if 'Item' in response:
                item = response['Item']
                try:
                    return json.loads(item['memory_value'])
                except:
                    return item['memory_value']
            return None
            
        except Exception as e:
            logger.error(f"Failed to get memory: {e}")
            return None
    
    async def delete_memory(
        self,
        session_id: str,
        key: str
    ) -> bool:
        """Delete conversation memory"""
        try:
            pk = self._get_memory_pk(session_id, key)
            
            self.table.delete_item(
                Key={
                    'PK': pk,
                    'SK': 'MEMORY'
                }
            )
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete memory: {e}")
            return False
    
    async def get_all_memories(
        self,
        session_id: str
    ) -> Dict[str, Any]:
        """Get all memories for a session"""
        try:
            response = self.table.query(
                IndexName='GSI1',
                KeyConditionExpression='GSI1PK = :session_id',
                ExpressionAttributeValues={
                    ':session_id': f"SESSION#{session_id}"
                }
            )
            
            memories = {}
            for item in response.get('Items', []):
                if item.get('SK') == 'MEMORY':
                    try:
                        memories[item['memory_key']] = json.loads(item['memory_value'])
                    except:
                        memories[item['memory_key']] = item['memory_value']
            
            return memories
            
        except Exception as e:
            logger.error(f"Failed to get all memories: {e}")
            return {}
