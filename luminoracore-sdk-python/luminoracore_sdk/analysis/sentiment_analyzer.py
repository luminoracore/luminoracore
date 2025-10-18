"""
Advanced Sentiment Analysis System

Real implementation of sentiment analysis using LLM providers.
"""

import asyncio
import json
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging

from ..session.storage_v1_1 import StorageV11Extension

logger = logging.getLogger(__name__)


@dataclass
class SentimentResult:
    """Result of sentiment analysis"""
    overall_sentiment: str
    sentiment_score: float
    emotions_detected: List[str]
    confidence: float
    analysis_timestamp: str
    message_count: int
    sentiment_trend: str
    detailed_analysis: Dict[str, Any]


class AdvancedSentimentAnalyzer:
    """
    Advanced sentiment analyzer using LLM providers for accurate analysis
    """
    
    def __init__(self, storage: StorageV11Extension, llm_provider=None):
        """
        Initialize sentiment analyzer
        
        Args:
            storage: Storage backend for persistence
            llm_provider: LLM provider for advanced analysis
        """
        self.storage = storage
        self.llm_provider = llm_provider
        
        # Sentiment thresholds
        self.POSITIVE_THRESHOLD = 0.6
        self.NEGATIVE_THRESHOLD = 0.4
        self.CONFIDENCE_THRESHOLD = 0.7
        
        # Emotion keywords
        self.EMOTION_KEYWORDS = {
            "joy": ["happy", "joyful", "excited", "cheerful", "delighted", "thrilled"],
            "sadness": ["sad", "depressed", "melancholy", "sorrowful", "gloomy", "dejected"],
            "anger": ["angry", "furious", "irritated", "annoyed", "frustrated", "enraged"],
            "fear": ["afraid", "scared", "worried", "anxious", "terrified", "nervous"],
            "surprise": ["surprised", "amazed", "shocked", "astonished", "stunned"],
            "disgust": ["disgusted", "revolted", "repulsed", "sickened", "appalled"],
            "trust": ["trust", "confident", "reliable", "faithful", "loyal"],
            "anticipation": ["excited", "eager", "hopeful", "optimistic", "enthusiastic"]
        }
        
        # Sentiment patterns
        self.SENTIMENT_PATTERNS = {
            "positive": [
                r"\b(good|great|excellent|amazing|wonderful|fantastic|awesome|perfect|love|like|enjoy|happy|pleased|satisfied)\b",
                r"\b(thank you|thanks|appreciate|grateful|pleased|delighted)\b"
            ],
            "negative": [
                r"\b(bad|terrible|awful|horrible|hate|dislike|angry|frustrated|annoyed|disappointed|upset)\b",
                r"\b(error|problem|issue|wrong|broken|failed|unsatisfactory)\b"
            ],
            "neutral": [
                r"\b(ok|okay|fine|alright|sure|maybe|perhaps|possibly)\b"
            ]
        }
    
    async def analyze_sentiment(
        self,
        session_id: str,
        user_id: str,
        **params
    ) -> SentimentResult:
        """
        Analyze sentiment of session conversations
        
        Args:
            session_id: Session identifier
            user_id: User identifier
            **params: Additional parameters
            
        Returns:
            SentimentResult with comprehensive analysis
        """
        try:
            logger.info(f"Starting sentiment analysis for session {session_id}")
            
            # Get conversation data
            conversation_data = await self._get_conversation_data(session_id, user_id)
            
            if not conversation_data:
                return self._create_no_data_result(session_id)
            
            # Perform multi-level analysis
            basic_analysis = self._perform_basic_analysis(conversation_data)
            advanced_analysis = await self._perform_advanced_analysis(conversation_data)
            emotion_analysis = self._perform_emotion_analysis(conversation_data)
            trend_analysis = await self._perform_trend_analysis(session_id, user_id)
            
            # Combine analyses
            combined_result = self._combine_analyses(
                basic_analysis, advanced_analysis, emotion_analysis, trend_analysis
            )
            
            # Create sentiment result
            result = SentimentResult(
                overall_sentiment=combined_result["overall_sentiment"],
                sentiment_score=combined_result["sentiment_score"],
                emotions_detected=combined_result["emotions_detected"],
                confidence=combined_result["confidence"],
                analysis_timestamp=datetime.now().isoformat(),
                message_count=len(conversation_data),
                sentiment_trend=combined_result["sentiment_trend"],
                detailed_analysis=combined_result["detailed_analysis"]
            )
            
            # Save analysis result
            await self._save_sentiment_analysis(session_id, user_id, result)
            
            logger.info(f"Sentiment analysis completed for session {session_id}")
            return result
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed for session {session_id}: {e}")
            return self._create_error_result(session_id, str(e))
    
    async def get_sentiment_history(
        self,
        session_id: str,
        user_id: str,
        limit: int = 10,
        include_details: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get sentiment analysis history
        
        Args:
            session_id: Session identifier
            user_id: User identifier
            limit: Maximum number of entries to return
            include_details: Whether to include detailed analysis
            
        Returns:
            List of sentiment analysis history entries
        """
        try:
            # Get sentiment history from storage
            history_key = f"sentiment_history_{user_id}"
            history_data = await self.storage.get_memory(session_id, history_key)
            
            if not history_data:
                return []
            
            history = json.loads(history_data) if isinstance(history_data, str) else history_data
            history = history.get('analyses', [])
            
            # Limit results
            if limit > 0:
                history = history[:limit]
            
            # Filter details if not requested
            if not include_details:
                for entry in history:
                    entry.pop('detailed_analysis', None)
            
            return history
            
        except Exception as e:
            logger.error(f"Failed to get sentiment history: {e}")
            return []
    
    async def _get_conversation_data(
        self,
        session_id: str,
        user_id: str
    ) -> List[Dict[str, Any]]:
        """Get conversation data for analysis"""
        try:
            # Get conversation from storage
            conversation_key = f"conversation_{session_id}"
            conversation_data = await self.storage.get_memory(session_id, conversation_key)
            
            if conversation_data:
                return json.loads(conversation_data) if isinstance(conversation_data, str) else conversation_data
            
            # Fallback: get from episodes and facts
            episodes = await self.storage.get_episodes(user_id)
            facts = await self.storage.get_facts(user_id)
            
            # Convert to conversation format
            conversation = []
            for episode in episodes:
                conversation.append({
                    "type": "episode",
                    "content": f"{episode['title']}: {episode['summary']}",
                    "sentiment": episode.get("sentiment", "neutral"),
                    "timestamp": episode.get("created_at", datetime.now().isoformat())
                })
            
            return conversation
            
        except Exception as e:
            logger.error(f"Failed to get conversation data: {e}")
            return []
    
    def _perform_basic_analysis(
        self,
        conversation_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Perform basic keyword-based sentiment analysis"""
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for message in conversation_data:
            content = message.get("content", "").lower()
            
            # Check positive patterns
            for pattern in self.SENTIMENT_PATTERNS["positive"]:
                if re.search(pattern, content, re.IGNORECASE):
                    positive_count += 1
                    break
            
            # Check negative patterns
            for pattern in self.SENTIMENT_PATTERNS["negative"]:
                if re.search(pattern, content, re.IGNORECASE):
                    negative_count += 1
                    break
            
            # Check neutral patterns
            for pattern in self.SENTIMENT_PATTERNS["neutral"]:
                if re.search(pattern, content, re.IGNORECASE):
                    neutral_count += 1
                    break
        
        total_messages = len(conversation_data)
        if total_messages == 0:
            return {
                "sentiment_score": 0.5,
                "confidence": 0.0,
                "positive_count": 0,
                "negative_count": 0,
                "neutral_count": 0
            }
        
        # Calculate sentiment score
        sentiment_score = (positive_count - negative_count) / total_messages
        sentiment_score = (sentiment_score + 1) / 2  # Normalize to 0-1
        
        # Determine overall sentiment
        if sentiment_score >= self.POSITIVE_THRESHOLD:
            overall_sentiment = "positive"
        elif sentiment_score <= self.NEGATIVE_THRESHOLD:
            overall_sentiment = "negative"
        else:
            overall_sentiment = "neutral"
        
        return {
            "sentiment_score": sentiment_score,
            "overall_sentiment": overall_sentiment,
            "confidence": min(0.8, (positive_count + negative_count) / total_messages),
            "positive_count": positive_count,
            "negative_count": negative_count,
            "neutral_count": neutral_count
        }
    
    async def _perform_advanced_analysis(
        self,
        conversation_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Perform advanced LLM-based sentiment analysis"""
        if not self.llm_provider:
            return {"advanced_analysis": "LLM provider not available"}
        
        try:
            # Prepare conversation text
            conversation_text = "\n".join([
                f"{msg.get('type', 'message')}: {msg.get('content', '')}"
                for msg in conversation_data[-10:]  # Last 10 messages
            ])
            
            # Create analysis prompt
            prompt = f"""
            Analyze the sentiment of the following conversation:
            
            {conversation_text}
            
            Provide analysis in this JSON format:
            {{
                "overall_sentiment": "positive/negative/neutral",
                "sentiment_score": 0.0-1.0,
                "confidence": 0.0-1.0,
                "key_emotions": ["emotion1", "emotion2"],
                "sentiment_indicators": ["indicator1", "indicator2"],
                "suggested_response_tone": "empathetic/technical/encouraging/neutral"
            }}
            """
            
            # Get LLM response
            response = await self.llm_provider.generate(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=300
            )
            
            # Parse response
            try:
                analysis = json.loads(response.content)
                return {
                    "llm_sentiment": analysis.get("overall_sentiment", "neutral"),
                    "llm_score": analysis.get("sentiment_score", 0.5),
                    "llm_confidence": analysis.get("confidence", 0.5),
                    "key_emotions": analysis.get("key_emotions", []),
                    "sentiment_indicators": analysis.get("sentiment_indicators", []),
                    "suggested_response_tone": analysis.get("suggested_response_tone", "neutral")
                }
            except json.JSONDecodeError:
                return {"advanced_analysis": "Failed to parse LLM response"}
                
        except Exception as e:
            logger.error(f"Advanced sentiment analysis failed: {e}")
            return {"advanced_analysis": f"LLM analysis failed: {str(e)}"}
    
    def _perform_emotion_analysis(
        self,
        conversation_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Perform emotion detection analysis"""
        emotion_counts = {}
        
        for message in conversation_data:
            content = message.get("content", "").lower()
            
            for emotion, keywords in self.EMOTION_KEYWORDS.items():
                for keyword in keywords:
                    if keyword in content:
                        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
                        break
        
        # Get top emotions
        top_emotions = sorted(
            emotion_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        return {
            "emotion_counts": emotion_counts,
            "top_emotions": [emotion for emotion, count in top_emotions if count > 0],
            "emotion_intensity": max(emotion_counts.values()) if emotion_counts else 0
        }
    
    async def _perform_trend_analysis(
        self,
        session_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """Perform sentiment trend analysis"""
        try:
            # Get recent sentiment history
            history = await self.get_sentiment_history(session_id, user_id, limit=5)
            
            if len(history) < 2:
                return {"trend": "insufficient_data"}
            
            # Calculate trend
            recent_scores = [entry.get("sentiment_score", 0.5) for entry in history[:3]]
            
            if len(recent_scores) >= 2:
                trend_direction = recent_scores[0] - recent_scores[-1]
                
                if trend_direction > 0.1:
                    trend = "improving"
                elif trend_direction < -0.1:
                    trend = "declining"
                else:
                    trend = "stable"
            else:
                trend = "insufficient_data"
            
            return {
                "trend": trend,
                "trend_magnitude": abs(trend_direction) if 'trend_direction' in locals() else 0,
                "recent_scores": recent_scores
            }
            
        except Exception as e:
            logger.error(f"Trend analysis failed: {e}")
            return {"trend": "analysis_failed"}
    
    def _combine_analyses(
        self,
        basic_analysis: Dict[str, Any],
        advanced_analysis: Dict[str, Any],
        emotion_analysis: Dict[str, Any],
        trend_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Combine all analyses into final result"""
        
        # Use advanced analysis if available, otherwise fall back to basic
        if "llm_sentiment" in advanced_analysis:
            overall_sentiment = advanced_analysis["llm_sentiment"]
            sentiment_score = advanced_analysis["llm_score"]
            confidence = advanced_analysis["llm_confidence"]
        else:
            overall_sentiment = basic_analysis["overall_sentiment"]
            sentiment_score = basic_analysis["sentiment_score"]
            confidence = basic_analysis["confidence"]
        
        # Combine emotions
        emotions_detected = emotion_analysis.get("top_emotions", [])
        if "key_emotions" in advanced_analysis:
            emotions_detected.extend(advanced_analysis["key_emotions"])
            emotions_detected = list(set(emotions_detected))  # Remove duplicates
        
        # Get trend
        sentiment_trend = trend_analysis.get("trend", "stable")
        
        # Create detailed analysis
        detailed_analysis = {
            "basic_analysis": basic_analysis,
            "advanced_analysis": advanced_analysis,
            "emotion_analysis": emotion_analysis,
            "trend_analysis": trend_analysis,
            "analysis_method": "combined"
        }
        
        return {
            "overall_sentiment": overall_sentiment,
            "sentiment_score": sentiment_score,
            "emotions_detected": emotions_detected,
            "confidence": confidence,
            "sentiment_trend": sentiment_trend,
            "detailed_analysis": detailed_analysis
        }
    
    async def _save_sentiment_analysis(
        self,
        session_id: str,
        user_id: str,
        result: SentimentResult
    ) -> bool:
        """Save sentiment analysis result"""
        try:
            # Save current analysis
            analysis_key = f"sentiment_analysis_{session_id}"
            await self.storage.save_memory(
                session_id,
                user_id,
                analysis_key,
                json.dumps({
                    "overall_sentiment": result.overall_sentiment,
                    "sentiment_score": result.sentiment_score,
                    "emotions_detected": result.emotions_detected,
                    "confidence": result.confidence,
                    "analysis_timestamp": result.analysis_timestamp,
                    "message_count": result.message_count,
                    "sentiment_trend": result.sentiment_trend
                })
            )
            
            # Save to history
            await self._save_sentiment_history(session_id, user_id, result)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to save sentiment analysis: {e}")
            return False
    
    async def _save_sentiment_history(
        self,
        session_id: str,
        user_id: str,
        result: SentimentResult
    ) -> bool:
        """Save sentiment analysis to history"""
        try:
            history_key = f"sentiment_history_{user_id}"
            
            # Get existing history
            existing_history = await self.storage.get_memory(session_id, history_key)
            history = {"analyses": []}
            
            if existing_history:
                history = json.loads(existing_history) if isinstance(existing_history, str) else existing_history
            
            # Add new analysis entry
            analysis_entry = {
                "timestamp": result.analysis_timestamp,
                "sentiment": result.overall_sentiment,
                "score": result.sentiment_score,
                "emotions": result.emotions_detected,
                "confidence": result.confidence,
                "message_count": result.message_count,
                "trend": result.sentiment_trend,
                "detailed_analysis": result.detailed_analysis
            }
            
            history["analyses"].insert(0, analysis_entry)  # Add to beginning
            
            # Keep only last 50 analyses
            if len(history["analyses"]) > 50:
                history["analyses"] = history["analyses"][:50]
            
            # Save updated history
            await self.storage.save_memory(
                session_id,
                user_id,
                history_key,
                json.dumps(history)
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to save sentiment history: {e}")
            return False
    
    def _create_no_data_result(self, session_id: str) -> SentimentResult:
        """Create result when no conversation data is available"""
        return SentimentResult(
            overall_sentiment="neutral",
            sentiment_score=0.5,
            emotions_detected=[],
            confidence=0.0,
            analysis_timestamp=datetime.now().isoformat(),
            message_count=0,
            sentiment_trend="no_data",
            detailed_analysis={"error": "No conversation data available"}
        )
    
    def _create_error_result(self, session_id: str, error: str) -> SentimentResult:
        """Create result when analysis fails"""
        return SentimentResult(
            overall_sentiment="neutral",
            sentiment_score=0.5,
            emotions_detected=[],
            confidence=0.0,
            analysis_timestamp=datetime.now().isoformat(),
            message_count=0,
            sentiment_trend="error",
            detailed_analysis={"error": error}
        )
