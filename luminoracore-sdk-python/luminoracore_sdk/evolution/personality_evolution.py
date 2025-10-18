"""
Personality Evolution System

Real implementation of personality evolution based on user interactions.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging

from ..session.storage_v1_1 import StorageV11Extension

logger = logging.getLogger(__name__)


@dataclass
class PersonalityChange:
    """Represents a change in personality traits"""
    trait_name: str
    old_value: float
    new_value: float
    change_reason: str
    confidence: float


@dataclass
class EvolutionResult:
    """Result of personality evolution analysis"""
    session_id: str
    evolution_timestamp: str
    changes_detected: bool
    personality_updates: Dict[str, Any]
    confidence_score: float
    changes: List[PersonalityChange]
    evolution_triggers: List[str]


class PersonalityEvolutionEngine:
    """
    Real personality evolution engine that analyzes user interactions
    and evolves personality traits accordingly.
    """
    
    def __init__(self, storage: StorageV11Extension):
        """
        Initialize personality evolution engine
        
        Args:
            storage: Storage backend for persistence
        """
        self.storage = storage
        
        # Evolution thresholds
        self.MIN_INTERACTIONS_FOR_EVOLUTION = 5
        self.AFFINITY_CHANGE_THRESHOLD = 10
        self.CONFIDENCE_THRESHOLD = 0.7
        
        # Personality trait weights
        self.TRAIT_WEIGHTS = {
            "formality": 0.8,
            "humor": 0.6,
            "empathy": 0.9,
            "directness": 0.7,
            "verbosity": 0.5,
            "warmth": 0.8,
            "patience": 0.7,
            "curiosity": 0.6
        }
    
    async def evolve_personality(
        self,
        session_id: str,
        user_id: str,
        personality_name: str,
        **params
    ) -> EvolutionResult:
        """
        Evolve personality based on session interactions
        
        Args:
            session_id: Session identifier
            user_id: User identifier
            personality_name: Personality being evolved
            **params: Additional parameters
            
        Returns:
            EvolutionResult with changes detected and applied
        """
        try:
            logger.info(f"Starting personality evolution for session {session_id}")
            
            # Get current personality state
            current_personality = await self._get_current_personality(user_id, personality_name)
            if not current_personality:
                return self._create_no_evolution_result(session_id, "No personality data found")
            
            # Analyze interaction patterns
            interaction_analysis = await self._analyze_interactions(session_id, user_id)
            
            # Check if evolution should occur
            evolution_triggers = await self._check_evolution_triggers(
                session_id, user_id, interaction_analysis
            )
            
            if not evolution_triggers:
                return self._create_no_evolution_result(session_id, "No evolution triggers detected")
            
            # Calculate personality changes
            personality_changes = await self._calculate_personality_changes(
                current_personality, interaction_analysis, evolution_triggers
            )
            
            if not personality_changes:
                return self._create_no_evolution_result(session_id, "No significant changes calculated")
            
            # Apply changes
            updated_personality = await self._apply_personality_changes(
                current_personality, personality_changes
            )
            
            # Save evolved personality
            await self._save_evolved_personality(user_id, personality_name, updated_personality)
            
            # Create evolution result
            result = EvolutionResult(
                session_id=session_id,
                evolution_timestamp=datetime.now().isoformat(),
                changes_detected=True,
                personality_updates=self._format_personality_updates(personality_changes),
                confidence_score=self._calculate_confidence_score(personality_changes),
                changes=personality_changes,
                evolution_triggers=evolution_triggers
            )
            
            logger.info(f"Personality evolution completed for session {session_id}")
            return result
            
        except Exception as e:
            logger.error(f"Personality evolution failed for session {session_id}: {e}")
            return self._create_no_evolution_result(session_id, f"Evolution failed: {str(e)}")
    
    async def get_evolution_history(
        self,
        session_id: str,
        user_id: str,
        limit: int = 10,
        include_details: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get personality evolution history
        
        Args:
            session_id: Session identifier
            user_id: User identifier
            limit: Maximum number of entries to return
            include_details: Whether to include detailed change information
            
        Returns:
            List of evolution history entries
        """
        try:
            # Get evolution history from storage
            evolution_key = f"evolution_history_{user_id}"
            history_data = await self.storage.get_memory(session_id, evolution_key)
            
            if not history_data:
                return []
            
            history = json.loads(history_data) if isinstance(history_data, str) else history_data
            history = history.get('evolutions', [])
            
            # Limit results
            if limit > 0:
                history = history[:limit]
            
            # Filter details if not requested
            if not include_details:
                for entry in history:
                    entry.pop('changes', None)
                    entry.pop('detailed_analysis', None)
            
            return history
            
        except Exception as e:
            logger.error(f"Failed to get evolution history: {e}")
            return []
    
    async def _get_current_personality(
        self,
        user_id: str,
        personality_name: str
    ) -> Optional[Dict[str, Any]]:
        """Get current personality configuration"""
        try:
            # Get personality from storage or default configuration
            personality_key = f"personality_{user_id}_{personality_name}"
            
            # Try to get from memory first
            personality_data = await self.storage.get_memory("global", personality_key)
            
            if personality_data:
                return json.loads(personality_data) if isinstance(personality_data, str) else personality_data
            
            # Return default personality if not found
            return self._get_default_personality(personality_name)
            
        except Exception as e:
            logger.error(f"Failed to get current personality: {e}")
            return self._get_default_personality(personality_name)
    
    async def _analyze_interactions(
        self,
        session_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """Analyze user interactions for evolution cues"""
        try:
            analysis = {
                "total_interactions": 0,
                "positive_interactions": 0,
                "negative_interactions": 0,
                "affinity_change": 0,
                "communication_patterns": {},
                "sentiment_trends": {},
                "response_preferences": {}
            }
            
            # Get affinity data
            affinity = await self.storage.get_affinity(user_id, "default")
            if affinity:
                analysis["affinity_change"] = affinity.get("affinity_points", 0)
                analysis["total_interactions"] = affinity.get("total_interactions", 0)
                analysis["positive_interactions"] = affinity.get("positive_interactions", 0)
            
            # Get facts for communication patterns
            facts = await self.storage.get_facts(user_id)
            for fact in facts:
                if fact["category"] == "communication_style":
                    analysis["communication_patterns"][fact["key"]] = fact["value"]
                elif fact["category"] == "preferences":
                    analysis["response_preferences"][fact["key"]] = fact["value"]
            
            # Get episodes for sentiment analysis
            episodes = await self.storage.get_episodes(user_id)
            sentiment_counts = {}
            for episode in episodes:
                sentiment = episode.get("sentiment", "neutral")
                sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
            
            analysis["sentiment_trends"] = sentiment_counts
            
            return analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze interactions: {e}")
            return {}
    
    async def _check_evolution_triggers(
        self,
        session_id: str,
        user_id: str,
        interaction_analysis: Dict[str, Any]
    ) -> List[str]:
        """Check if evolution should be triggered"""
        triggers = []
        
        # Check interaction count
        if interaction_analysis.get("total_interactions", 0) >= self.MIN_INTERACTIONS_FOR_EVOLUTION:
            triggers.append("sufficient_interactions")
        
        # Check affinity change
        if abs(interaction_analysis.get("affinity_change", 0)) >= self.AFFINITY_CHANGE_THRESHOLD:
            triggers.append("significant_affinity_change")
        
        # Check sentiment trends
        sentiment_trends = interaction_analysis.get("sentiment_trends", {})
        if sentiment_trends.get("positive", 0) > sentiment_trends.get("negative", 0) * 2:
            triggers.append("positive_sentiment_dominance")
        elif sentiment_trends.get("negative", 0) > sentiment_trends.get("positive", 0) * 2:
            triggers.append("negative_sentiment_dominance")
        
        # Check communication patterns
        comm_patterns = interaction_analysis.get("communication_patterns", {})
        if len(comm_patterns) >= 3:
            triggers.append("established_communication_patterns")
        
        return triggers
    
    async def _calculate_personality_changes(
        self,
        current_personality: Dict[str, Any],
        interaction_analysis: Dict[str, Any],
        evolution_triggers: List[str]
    ) -> List[PersonalityChange]:
        """Calculate specific personality trait changes"""
        changes = []
        
        current_traits = current_personality.get("advanced_parameters", {})
        
        # Calculate changes based on triggers
        for trigger in evolution_triggers:
            if trigger == "positive_sentiment_dominance":
                # Increase warmth and empathy
                changes.extend(self._calculate_warmth_increase(current_traits))
                changes.extend(self._calculate_empathy_increase(current_traits))
                
            elif trigger == "negative_sentiment_dominance":
                # Increase patience and formality
                changes.extend(self._calculate_patience_increase(current_traits))
                changes.extend(self._calculate_formality_increase(current_traits))
                
            elif trigger == "significant_affinity_change":
                # Adjust based on affinity direction
                affinity_change = interaction_analysis.get("affinity_change", 0)
                if affinity_change > 0:
                    # Increase warmth and decrease formality
                    changes.extend(self._calculate_warmth_increase(current_traits))
                    changes.extend(self._calculate_formality_decrease(current_traits))
                else:
                    # Increase formality and patience
                    changes.extend(self._calculate_formality_increase(current_traits))
                    changes.extend(self._calculate_patience_increase(current_traits))
        
        # Filter out insignificant changes
        significant_changes = [
            change for change in changes 
            if abs(change.new_value - change.old_value) >= 0.1
        ]
        
        return significant_changes
    
    def _calculate_warmth_increase(self, current_traits: Dict[str, Any]) -> List[PersonalityChange]:
        """Calculate warmth increase changes"""
        changes = []
        current_warmth = current_traits.get("warmth", 0.5)
        
        if current_warmth < 0.8:
            new_warmth = min(0.8, current_warmth + 0.1)
            changes.append(PersonalityChange(
                trait_name="warmth",
                old_value=current_warmth,
                new_value=new_warmth,
                change_reason="positive_interaction_pattern",
                confidence=0.8
            ))
        
        return changes
    
    def _calculate_empathy_increase(self, current_traits: Dict[str, Any]) -> List[PersonalityChange]:
        """Calculate empathy increase changes"""
        changes = []
        current_empathy = current_traits.get("empathy", 0.5)
        
        if current_empathy < 0.9:
            new_empathy = min(0.9, current_empathy + 0.1)
            changes.append(PersonalityChange(
                trait_name="empathy",
                old_value=current_empathy,
                new_value=new_empathy,
                change_reason="positive_sentiment_detected",
                confidence=0.85
            ))
        
        return changes
    
    def _calculate_patience_increase(self, current_traits: Dict[str, Any]) -> List[PersonalityChange]:
        """Calculate patience increase changes"""
        changes = []
        current_patience = current_traits.get("patience", 0.5)
        
        if current_patience < 0.8:
            new_patience = min(0.8, current_patience + 0.1)
            changes.append(PersonalityChange(
                trait_name="patience",
                old_value=current_patience,
                new_value=new_patience,
                change_reason="negative_sentiment_detected",
                confidence=0.75
            ))
        
        return changes
    
    def _calculate_formality_increase(self, current_traits: Dict[str, Any]) -> List[PersonalityChange]:
        """Calculate formality increase changes"""
        changes = []
        current_formality = current_traits.get("formality", 0.5)
        
        if current_formality < 0.8:
            new_formality = min(0.8, current_formality + 0.1)
            changes.append(PersonalityChange(
                trait_name="formality",
                old_value=current_formality,
                new_value=new_formality,
                change_reason="negative_interaction_pattern",
                confidence=0.7
            ))
        
        return changes
    
    def _calculate_formality_decrease(self, current_traits: Dict[str, Any]) -> List[PersonalityChange]:
        """Calculate formality decrease changes"""
        changes = []
        current_formality = current_traits.get("formality", 0.5)
        
        if current_formality > 0.2:
            new_formality = max(0.2, current_formality - 0.1)
            changes.append(PersonalityChange(
                trait_name="formality",
                old_value=current_formality,
                new_value=new_formality,
                change_reason="positive_affinity_growth",
                confidence=0.8
            ))
        
        return changes
    
    async def _apply_personality_changes(
        self,
        current_personality: Dict[str, Any],
        changes: List[PersonalityChange]
    ) -> Dict[str, Any]:
        """Apply calculated changes to personality"""
        updated_personality = current_personality.copy()
        advanced_params = updated_personality.get("advanced_parameters", {}).copy()
        
        for change in changes:
            advanced_params[change.trait_name] = change.new_value
        
        updated_personality["advanced_parameters"] = advanced_params
        updated_personality["last_evolution"] = {
            "timestamp": datetime.now().isoformat(),
            "changes_count": len(changes),
            "confidence_score": self._calculate_confidence_score(changes)
        }
        
        return updated_personality
    
    async def _save_evolved_personality(
        self,
        user_id: str,
        personality_name: str,
        evolved_personality: Dict[str, Any]
    ) -> bool:
        """Save evolved personality to storage"""
        try:
            personality_key = f"personality_{user_id}_{personality_name}"
            await self.storage.save_memory(
                "global",
                user_id,
                personality_key,
                json.dumps(evolved_personality)
            )
            
            # Save evolution history
            await self._save_evolution_history(user_id, evolved_personality)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to save evolved personality: {e}")
            return False
    
    async def _save_evolution_history(
        self,
        user_id: str,
        evolved_personality: Dict[str, Any]
    ) -> bool:
        """Save evolution to history"""
        try:
            history_key = f"evolution_history_{user_id}"
            
            # Get existing history
            existing_history = await self.storage.get_memory("global", history_key)
            history = {"evolutions": []}
            
            if existing_history:
                history = json.loads(existing_history) if isinstance(existing_history, str) else existing_history
            
            # Add new evolution entry
            evolution_entry = {
                "timestamp": datetime.now().isoformat(),
                "changes": [
                    {
                        "trait": change.get("trait_name"),
                        "old_value": change.get("old_value"),
                        "new_value": change.get("new_value"),
                        "reason": change.get("change_reason")
                    }
                    for change in evolved_personality.get("last_evolution", {}).get("changes", [])
                ],
                "confidence_score": evolved_personality.get("last_evolution", {}).get("confidence_score", 0.0)
            }
            
            history["evolutions"].insert(0, evolution_entry)  # Add to beginning
            
            # Keep only last 50 evolutions
            if len(history["evolutions"]) > 50:
                history["evolutions"] = history["evolutions"][:50]
            
            # Save updated history
            await self.storage.save_memory(
                "global",
                user_id,
                history_key,
                json.dumps(history)
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to save evolution history: {e}")
            return False
    
    def _get_default_personality(self, personality_name: str) -> Dict[str, Any]:
        """Get default personality configuration"""
        return {
            "name": personality_name,
            "advanced_parameters": {
                "formality": 0.5,
                "humor": 0.5,
                "empathy": 0.5,
                "directness": 0.5,
                "verbosity": 0.5,
                "warmth": 0.5,
                "patience": 0.5,
                "curiosity": 0.5
            },
            "created_at": datetime.now().isoformat()
        }
    
    def _format_personality_updates(self, changes: List[PersonalityChange]) -> Dict[str, Any]:
        """Format personality updates for response"""
        updates = {}
        
        for change in changes:
            if change.trait_name == "formality":
                if change.new_value > change.old_value:
                    updates["communication_style"] = "more_formal"
                else:
                    updates["communication_style"] = "more_casual"
            elif change.trait_name == "empathy":
                updates["emotional_tone"] = "more_empathetic"
            elif change.trait_name == "verbosity":
                if change.new_value > change.old_value:
                    updates["response_length"] = "increased"
                else:
                    updates["response_length"] = "decreased"
        
        return updates
    
    def _calculate_confidence_score(self, changes: List[PersonalityChange]) -> float:
        """Calculate overall confidence score for evolution"""
        if not changes:
            return 0.0
        
        total_confidence = sum(change.confidence for change in changes)
        return min(1.0, total_confidence / len(changes))
    
    def _create_no_evolution_result(
        self,
        session_id: str,
        reason: str
    ) -> EvolutionResult:
        """Create result when no evolution occurs"""
        return EvolutionResult(
            session_id=session_id,
            evolution_timestamp=datetime.now().isoformat(),
            changes_detected=False,
            personality_updates={},
            confidence_score=0.0,
            changes=[],
            evolution_triggers=[reason]
        )
