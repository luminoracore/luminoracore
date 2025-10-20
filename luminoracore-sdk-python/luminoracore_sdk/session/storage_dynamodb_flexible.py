"""
Flexible DynamoDB Storage v11 Implementation

This implementation adapts to ANY DynamoDB table schema.
The user can use their own tables with their own schemas.
"""

import json
import boto3
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, timedelta
import logging
from botocore.exceptions import ClientError
from decimal import Decimal

from .storage_v1_1 import StorageV11Extension

logger = logging.getLogger(__name__)


def _convert_floats_to_decimal(obj):
    """Convert floats to Decimal for DynamoDB compatibility"""
    if isinstance(obj, float):
        return Decimal(str(obj))
    elif isinstance(obj, dict):
        return {key: _convert_floats_to_decimal(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [_convert_floats_to_decimal(item) for item in obj]
    else:
        return obj


class FlexibleDynamoDBStorageV11(StorageV11Extension):
    """
    Flexible DynamoDB storage that adapts to ANY table schema
    
    The user can use their own DynamoDB tables with any schema.
    This implementation automatically detects and adapts to the table structure.
    """
    
    def __init__(
        self, 
        table_name: str, 
        region_name: str = "us-east-1",
        hash_key_name: str = None,
        range_key_name: str = None,
        gsi_name: str = None,
        gsi_hash_key: str = None,
        gsi_range_key: str = None
    ):
        """
        Initialize flexible DynamoDB storage
        
        Args:
            table_name: DynamoDB table name (user's table)
            region_name: AWS region name
            hash_key_name: Name of the hash key (auto-detected if None)
            range_key_name: Name of the range key (auto-detected if None)
            gsi_name: Name of Global Secondary Index (auto-detected if None)
            gsi_hash_key: Name of GSI hash key (auto-detected if None)
            gsi_range_key: Name of GSI range key (auto-detected if None)
        """
        self.table_name = table_name
        self.region_name = region_name
        
        try:
            self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
            self.table = self.dynamodb.Table(table_name)
            
            # Auto-detect table schema
            self._detect_table_schema()
            
            # Use provided schema or detected schema
            self.hash_key_name = hash_key_name or self.detected_hash_key
            self.range_key_name = range_key_name or self.detected_range_key
            self.gsi_name = gsi_name or self.detected_gsi_name
            self.gsi_hash_key = gsi_hash_key or self.detected_gsi_hash_key
            self.gsi_range_key = gsi_range_key or self.detected_gsi_range_key
            
            logger.info(f"Flexible DynamoDB storage initialized with table: {table_name}")
            logger.info(f"Schema: {self.hash_key_name}/{self.range_key_name}, GSI: {self.gsi_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize flexible DynamoDB storage: {e}")
            raise
    
    def _detect_table_schema(self):
        """Auto-detect the table schema"""
        try:
            response = self.table.meta.client.describe_table(TableName=self.table_name)
            table_info = response['Table']
            
            # Detect primary key schema
            key_schema = table_info['KeySchema']
            self.detected_hash_key = key_schema[0]['AttributeName']
            self.detected_range_key = key_schema[1]['AttributeName'] if len(key_schema) > 1 else None
            
            # Detect GSI schema
            gsis = table_info.get('GlobalSecondaryIndexes', [])
            if gsis:
                gsi = gsis[0]  # Use first GSI
                self.detected_gsi_name = gsi['IndexName']
                gsi_keys = gsi['KeySchema']
                self.detected_gsi_hash_key = gsi_keys[0]['AttributeName']
                self.detected_gsi_range_key = gsi_keys[1]['AttributeName'] if len(gsi_keys) > 1 else None
            else:
                self.detected_gsi_name = None
                self.detected_gsi_hash_key = None
                self.detected_gsi_range_key = None
                
            logger.info(f"Detected schema: {self.detected_hash_key}/{self.detected_range_key}")
            if self.detected_gsi_name:
                logger.info(f"Detected GSI: {self.detected_gsi_name} ({self.detected_gsi_hash_key}/{self.detected_gsi_range_key})")
                
        except Exception as e:
            logger.error(f"Failed to detect table schema: {e}")
            # Fallback to common schema names
            self.detected_hash_key = 'PK'
            self.detected_range_key = 'SK'
            self.detected_gsi_name = None
            self.detected_gsi_hash_key = None
            self.detected_gsi_range_key = None
    
    def _generate_key_values(self, user_id: str, category: str, key: str, item_type: str = "FACT") -> Dict[str, str]:
        """Generate key values based on detected schema"""
        
        # Common patterns for different schema types
        if self.hash_key_name in ['session_id', 'id', 'pk']:
            # Simple session-based schema
            hash_value = user_id
            range_value = f"{item_type}#{category}#{key}"
        elif self.hash_key_name in ['PK', 'pk', 'partition_key']:
            # Partition key schema
            hash_value = f"{item_type}#{user_id}#{category}#{key}"
            range_value = item_type
        else:
            # Generic schema - use detected names
            hash_value = user_id
            range_value = f"{item_type}#{category}#{key}"
        
        return {
            self.hash_key_name: hash_value,
            self.range_key_name: range_value
        }
    
    def _generate_gsi_values(self, user_id: str, category: str) -> Dict[str, str]:
        """Generate GSI values if GSI exists"""
        if not self.gsi_name:
            return {}
        
        if self.gsi_hash_key in ['GSI1PK', 'gsi1pk', 'user_id']:
            gsi_hash_value = f"USER#{user_id}"
            gsi_range_value = f"CATEGORY#{category}"
        else:
            gsi_hash_value = user_id
            gsi_range_value = category
        
        return {
            self.gsi_hash_key: gsi_hash_value,
            self.gsi_range_key: gsi_range_value
        }
    
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
            key_values = self._generate_key_values(user_id, personality_name, "affinity", "AFFINITY")
            gsi_values = self._generate_gsi_values(user_id, personality_name)
            
            item = {
                **key_values,
                **gsi_values,
                'user_id': user_id,
                'session_id': kwargs.get('session_id', user_id),
                'personality_name': personality_name,
                'affinity_points': affinity_points,
                'current_level': current_level,
                'total_interactions': kwargs.get('total_interactions', 0),
                'positive_interactions': kwargs.get('positive_interactions', 0),
                'created_at': kwargs.get('created_at', datetime.now().isoformat()),
                'updated_at': datetime.now().isoformat(),
                'TTL': int((datetime.now() + timedelta(days=365)).timestamp())
            }
            
            # Convert floats to Decimal for DynamoDB compatibility
            item = _convert_floats_to_decimal(item)
            
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
        """Get user affinity"""
        try:
            key_values = self._generate_key_values(user_id, personality_name, "affinity", "AFFINITY")
            
            response = self.table.get_item(Key=key_values)
            
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
            key_values = self._generate_key_values(user_id, category, key, "FACT")
            gsi_values = self._generate_gsi_values(user_id, category)
            
            item = {
                **key_values,
                **gsi_values,
                'user_id': user_id,
                'session_id': kwargs.get('session_id', user_id),
                'category': category,
                'key': key,
                'value': json.dumps(value) if not isinstance(value, str) else value,
                'confidence': kwargs.get('confidence', 1.0),
                'created_at': kwargs.get('created_at', datetime.now().isoformat()),
                'updated_at': datetime.now().isoformat(),
                'TTL': int((datetime.now() + timedelta(days=365)).timestamp())
            }
            
            # Convert floats to Decimal for DynamoDB compatibility
            item = _convert_floats_to_decimal(item)
            
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
            if category and self.gsi_name:
                # Query by category using GSI
                response = self.table.query(
                    IndexName=self.gsi_name,
                    KeyConditionExpression=f'{self.gsi_hash_key} = :user_id AND begins_with({self.gsi_range_key}, :category)',
                    ExpressionAttributeValues={
                        ':user_id': f"USER#{user_id}",
                        ':category': f"CATEGORY#{category}"
                    }
                )
            elif self.gsi_name:
                # Query all facts for user using GSI
                response = self.table.query(
                    IndexName=self.gsi_name,
                    KeyConditionExpression=f'{self.gsi_hash_key} = :user_id',
                    ExpressionAttributeValues={
                        ':user_id': f"USER#{user_id}"
                    }
                )
            else:
                # Scan table (less efficient but works with any schema)
                # Use ExpressionAttributeNames to handle reserved keywords
                response = self.table.scan(
                    FilterExpression='user_id = :user_id AND begins_with(#range_key, :fact_prefix)',
                    ExpressionAttributeNames={
                        '#range_key': self.range_key_name
                    },
                    ExpressionAttributeValues={
                        ':user_id': user_id,
                        ':fact_prefix': 'FACT#'
                    }
                )
            
            facts = []
            for item in response.get('Items', []):
                if item.get('key') and item.get('category'):
                    try:
                        fact_value = item['value']
                        if isinstance(fact_value, str):
                            try:
                                fact_value = json.loads(fact_value)
                            except:
                                pass  # Keep as string if not JSON
                        
                        facts.append({
                            'category': item['category'],
                            'key': item['key'],
                            'value': fact_value,
                            'confidence': float(item.get('confidence', 1.0)),
                            'created_at': item.get('created_at'),
                            'updated_at': item.get('updated_at')
                        })
                    except Exception as e:
                        logger.warning(f"Failed to parse fact item: {e}")
                        continue
            
            return facts
            
        except Exception as e:
            logger.error(f"Failed to get facts: {e}")
            return []
    
    async def delete_fact(
        self,
        user_id: str,
        category: str,
        key: str
    ) -> bool:
        """Delete a user fact"""
        try:
            key_values = self._generate_key_values(user_id, category, key, "FACT")
            self.table.delete_item(Key=key_values)
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete fact: {e}")
            return False
    
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
        """Save a memorable episode"""
        try:
            episode_id = f"{episode_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            key_values = self._generate_key_values(user_id, episode_type, episode_id, "EPISODE")
            gsi_values = self._generate_gsi_values(user_id, episode_type)
            
            item = {
                **key_values,
                **gsi_values,
                'user_id': user_id,
                'session_id': kwargs.get('session_id', user_id),
                'episode_type': episode_type,
                'title': title,
                'summary': summary,
                'importance': importance,
                'sentiment': sentiment,
                'created_at': kwargs.get('created_at', datetime.now().isoformat()),
                'updated_at': datetime.now().isoformat(),
                'TTL': int((datetime.now() + timedelta(days=365)).timestamp())
            }
            
            # Convert floats to Decimal for DynamoDB compatibility
            item = _convert_floats_to_decimal(item)
            
            self.table.put_item(Item=item)
            return True
            
        except Exception as e:
            logger.error(f"Failed to save episode: {e}")
            return False
    
    async def get_episodes(
        self,
        user_id: str,
        min_importance: Optional[float] = None,
        max_results: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get user episodes"""
        try:
            if self.gsi_name:
                # Query using GSI
                response = self.table.query(
                    IndexName=self.gsi_name,
                    KeyConditionExpression=f'{self.gsi_hash_key} = :user_id',
                    ExpressionAttributeValues={
                        ':user_id': f"USER#{user_id}"
                    }
                )
            else:
                # Scan table
                response = self.table.scan(
                    FilterExpression='user_id = :user_id AND begins_with(#range_key, :episode_prefix)',
                    ExpressionAttributeNames={
                        '#range_key': self.range_key_name
                    },
                    ExpressionAttributeValues={
                        ':user_id': user_id,
                        ':episode_prefix': 'EPISODE#'
                    }
                )
            
            episodes = []
            for item in response.get('Items', []):
                if item.get('episode_type') and item.get('title'):
                    try:
                        importance = float(item.get('importance', 0.0))
                        if min_importance is not None and importance < min_importance:
                            continue
                        
                        episodes.append({
                            'episode_type': item['episode_type'],
                            'title': item['title'],
                            'summary': item['summary'],
                            'importance': importance,
                            'sentiment': item['sentiment'],
                            'created_at': item.get('created_at'),
                            'updated_at': item.get('updated_at')
                        })
                    except Exception as e:
                        logger.warning(f"Failed to parse episode item: {e}")
                        continue
            
            # Sort by importance and limit results
            episodes.sort(key=lambda x: x['importance'], reverse=True)
            if max_results:
                episodes = episodes[:max_results]
            
            return episodes
            
        except Exception as e:
            logger.error(f"Failed to get episodes: {e}")
            return []
    
    # MOOD METHODS
    async def save_mood(
        self,
        user_id: str,
        mood_type: str,
        intensity: float,
        context: str,
        **kwargs
    ) -> bool:
        """Save user mood"""
        try:
            mood_id = f"{mood_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            key_values = self._generate_key_values(user_id, "mood", mood_id, "MOOD")
            gsi_values = self._generate_gsi_values(user_id, "mood")
            
            item = {
                **key_values,
                **gsi_values,
                'user_id': user_id,
                'session_id': kwargs.get('session_id', user_id),
                'mood_type': mood_type,
                'intensity': intensity,
                'context': context,
                'created_at': kwargs.get('created_at', datetime.now().isoformat()),
                'updated_at': datetime.now().isoformat(),
                'TTL': int((datetime.now() + timedelta(days=30)).timestamp())
            }
            
            # Convert floats to Decimal for DynamoDB compatibility
            item = _convert_floats_to_decimal(item)
            
            self.table.put_item(Item=item)
            return True
            
        except Exception as e:
            logger.error(f"Failed to save mood: {e}")
            return False
    
    async def get_mood(
        self,
        user_id: str,
        personality_name: str
    ) -> Optional[Dict[str, Any]]:
        """Get current mood for user and personality"""
        try:
            # Get latest mood from history
            mood_history = await self.get_mood_history(user_id, days_back=1)
            if mood_history:
                latest_mood = mood_history[0]  # Most recent mood
                return {
                    'mood_type': latest_mood['mood_type'],
                    'intensity': latest_mood['intensity'],
                    'context': latest_mood['context'],
                    'timestamp': latest_mood['created_at']
                }
            return None
            
        except Exception as e:
            logger.error(f"Failed to get mood: {e}")
            return None
    
    async def get_mood_history(
        self,
        user_id: str,
        mood_type: Optional[str] = None,
        days_back: int = 30
    ) -> List[Dict[str, Any]]:
        """Get user mood history"""
        try:
            if self.gsi_name:
                # Query using GSI
                response = self.table.query(
                    IndexName=self.gsi_name,
                    KeyConditionExpression=f'{self.gsi_hash_key} = :user_id',
                    ExpressionAttributeValues={
                        ':user_id': f"USER#{user_id}"
                    }
                )
            else:
                # Scan table
                response = self.table.scan(
                    FilterExpression='user_id = :user_id AND begins_with(#range_key, :mood_prefix)',
                    ExpressionAttributeNames={
                        '#range_key': self.range_key_name
                    },
                    ExpressionAttributeValues={
                        ':user_id': user_id,
                        ':mood_prefix': 'MOOD#'
                    }
                )
            
            moods = []
            cutoff_date = datetime.now() - timedelta(days=days_back)
            
            for item in response.get('Items', []):
                if item.get('mood_type') and item.get('intensity') is not None:
                    try:
                        if mood_type and item['mood_type'] != mood_type:
                            continue
                        
                        created_at = item.get('created_at')
                        if created_at:
                            try:
                                item_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                                if item_date < cutoff_date:
                                    continue
                            except:
                                pass  # Include if date parsing fails
                        
                        moods.append({
                            'mood_type': item['mood_type'],
                            'intensity': float(item['intensity']),
                            'context': item.get('context', ''),
                            'created_at': created_at,
                            'updated_at': item.get('updated_at')
                        })
                    except Exception as e:
                        logger.warning(f"Failed to parse mood item: {e}")
                        continue
            
            # Sort by date
            moods.sort(key=lambda x: x['created_at'] or '', reverse=True)
            return moods
            
        except Exception as e:
            logger.error(f"Failed to get mood history: {e}")
            return []
    
    # MEMORY METHODS
    async def save_memory(
        self,
        user_id: str,
        memory_key: str,
        memory_value: Any,
        **kwargs
    ) -> bool:
        """Save a memory item"""
        try:
            key_values = self._generate_key_values(user_id, "memory", memory_key, "MEMORY")
            gsi_values = self._generate_gsi_values(user_id, "memory")
            
            item = {
                **key_values,
                **gsi_values,
                'user_id': user_id,
                'session_id': kwargs.get('session_id', user_id),
                'memory_key': memory_key,
                'memory_value': json.dumps(memory_value) if not isinstance(memory_value, str) else memory_value,
                'created_at': kwargs.get('created_at', datetime.now().isoformat()),
                'updated_at': datetime.now().isoformat(),
                'TTL': int((datetime.now() + timedelta(days=365)).timestamp())
            }
            
            # Convert floats to Decimal for DynamoDB compatibility
            item = _convert_floats_to_decimal(item)
            
            self.table.put_item(Item=item)
            return True
            
        except Exception as e:
            logger.error(f"Failed to save memory: {e}")
            return False
    
    async def get_memory(
        self,
        user_id: str,
        memory_key: str
    ) -> Optional[Any]:
        """Get a memory item"""
        try:
            key_values = self._generate_key_values(user_id, "memory", memory_key, "MEMORY")
            
            response = self.table.get_item(Key=key_values)
            
            if 'Item' in response:
                memory_value = response['Item']['memory_value']
                try:
                    return json.loads(memory_value)
                except:
                    return memory_value
            return None
            
        except Exception as e:
            logger.error(f"Failed to get memory: {e}")
            return None
    
    async def delete_memory(
        self,
        user_id: str,
        memory_key: str
    ) -> bool:
        """Delete a memory item"""
        try:
            key_values = self._generate_key_values(user_id, "memory", memory_key, "MEMORY")
            self.table.delete_item(Key=key_values)
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete memory: {e}")
            return False
