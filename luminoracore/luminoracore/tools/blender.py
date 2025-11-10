"""
Personality blender for LuminoraCore.
"""

import json
from typing import Dict, Any, List, Optional, Union, Tuple
from pathlib import Path
import logging
from dataclasses import dataclass, asdict
import random

from ..core.personality import Personality, PersonalityError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class BlendWeights:
    """Weights for personality blending."""
    weights: Dict[str, float]
    
    def __post_init__(self):
        """Validate and normalize weights."""
        total_weight = sum(self.weights.values())
        if total_weight == 0:
            raise PersonalityError("Total weight cannot be zero")
        
        # Normalize weights
        self.weights = {name: weight / total_weight for name, weight in self.weights.items()}
    
    def get_weight(self, name: str) -> float:
        """Get weight for a personality."""
        return self.weights.get(name, 0.0)


@dataclass
class BlendResult:
    """Result of personality blending."""
    blended_personality: Personality
    blend_info: Dict[str, Any]
    weights: BlendWeights


class PersonaBlend:
    """Blends multiple personalities with specified weights."""
    
    def __init__(self):
        """Initialize the blender."""
        self.blend_strategies = {
            "weighted_average": self._weighted_average_blend,
            "dominant": self._dominant_blend,
            "hybrid": self._hybrid_blend,
            "random": self._random_blend,
        }
    
    def blend(self, personalities: List[Personality], 
              weights: Union[Dict[str, float], BlendWeights],
              strategy: str = "weighted_average",
              name: Optional[str] = None) -> BlendResult:
        """
        Blend multiple personalities.
        
        Args:
            personalities: List of Personality objects to blend
            weights: Weights for each personality (dict or BlendWeights)
            strategy: Blending strategy to use
            name: Name for the blended personality
            
        Returns:
            BlendResult with blended personality
        """
        try:
            # Validate inputs
            if len(personalities) < 2:
                raise PersonalityError("Need at least 2 personalities to blend")
            
            if len(personalities) != len(weights):
                raise PersonalityError("Number of personalities must match number of weights")
            
            # Convert weights to BlendWeights
            if isinstance(weights, dict):
                blend_weights = BlendWeights(weights)
            else:
                blend_weights = weights
            
            # Get blending strategy
            if strategy not in self.blend_strategies:
                raise PersonalityError(f"Unknown blending strategy: {strategy}")
            
            blend_func = self.blend_strategies[strategy]
            
            # Perform blending
            blended_data = blend_func(personalities, blend_weights)
            
            # Set name if provided
            if name:
                blended_data["persona"]["name"] = name
            else:
                blended_data["persona"]["name"] = self._generate_blend_name(personalities, blend_weights)
            
            # Update metadata
            blended_data["persona"]["description"] = self._generate_blend_description(personalities, blend_weights)
            blended_data["persona"]["author"] = "PersonaBlend"
            blended_data["persona"]["tags"] = self._blend_tags(personalities, blend_weights)
            
            # Create blended personality
            blended_personality = Personality(blended_data)
            
            # Create blend info
            blend_info = {
                "strategy": strategy,
                "source_personalities": [p.persona.name for p in personalities],
                "weights": blend_weights.weights,
                "created_at": blended_data.get("metadata", {}).get("created_at"),
                "version": "1.0.0"
            }
            
            return BlendResult(
                blended_personality=blended_personality,
                blend_info=blend_info,
                weights=blend_weights
            )
            
        except Exception as e:
            logger.error(f"Blending failed: {e}")
            raise PersonalityError(f"Failed to blend personalities: {e}")
    
    def _weighted_average_blend(self, personalities: List[Personality], weights: BlendWeights) -> Dict[str, Any]:
        """Blend using weighted average of all components."""
        blended = {}
        
        # Get all unique keys from all personalities
        all_keys = set()
        for personality in personalities:
            all_keys.update(personality.to_dict().keys())
        
        for key in all_keys:
            if key == "persona":
                blended[key] = self._blend_persona(personalities, weights)
            elif key == "core_traits":
                blended[key] = self._blend_core_traits(personalities, weights)
            elif key == "linguistic_profile":
                blended[key] = self._blend_linguistic_profile(personalities, weights)
            elif key == "behavioral_rules":
                blended[key] = self._blend_behavioral_rules(personalities, weights)
            elif key == "trigger_responses":
                blended[key] = self._blend_trigger_responses(personalities, weights)
            elif key == "advanced_parameters":
                blended[key] = self._blend_advanced_parameters(personalities, weights)
            elif key == "safety_guards":
                blended[key] = self._blend_safety_guards(personalities, weights)
            elif key == "examples":
                blended[key] = self._blend_examples(personalities, weights)
            elif key == "metadata":
                blended[key] = self._blend_metadata(personalities, weights)
        
        return blended
    
    def _dominant_blend(self, personalities: List[Personality], weights: BlendWeights) -> Dict[str, Any]:
        """Blend using the dominant personality with some influence from others."""
        # Find dominant personality
        dominant_name = max(weights.weights.keys(), key=lambda k: weights.weights[k])
        dominant_personality = next(p for p in personalities if p.persona.name == dominant_name)
        
        # Start with dominant personality
        blended = dominant_personality.to_dict().copy()
        
        # Apply some influence from other personalities (reduced weight)
        other_personalities = [p for p in personalities if p.persona.name != dominant_name]
        other_weights = BlendWeights({
            p.persona.name: weights.get_weight(p.persona.name) * 0.3 
            for p in other_personalities
        })
        
        if other_personalities:
            other_influence = self._weighted_average_blend(other_personalities, other_weights)
            blended = self._merge_dicts(blended, other_influence, 0.2)
        
        return blended
    
    def _hybrid_blend(self, personalities: List[Personality], weights: BlendWeights) -> Dict[str, Any]:
        """Blend using hybrid approach - some components averaged, others selected."""
        blended = {}
        
        # Average these components
        avg_components = ["linguistic_profile", "advanced_parameters", "safety_guards"]
        for key in avg_components:
            blended[key] = self._blend_component(personalities, weights, key)
        
        # Select dominant for these components
        dominant_name = max(weights.weights.keys(), key=lambda k: weights.weights[k])
        dominant_personality = next(p for p in personalities if p.persona.name == dominant_name)
        dominant_data = dominant_personality.to_dict()
        
        select_components = ["persona", "core_traits", "behavioral_rules"]
        for key in select_components:
            if key in dominant_data:
                blended[key] = dominant_data[key].copy()
        
        # Blend trigger responses and examples
        blended["trigger_responses"] = self._blend_trigger_responses(personalities, weights)
        blended["examples"] = self._blend_examples(personalities, weights)
        blended["metadata"] = self._blend_metadata(personalities, weights)
        
        return blended
    
    def _random_blend(self, personalities: List[Personality], weights: BlendWeights) -> Dict[str, Any]:
        """Blend using random selection weighted by importance."""
        blended = {}
        
        # Get all unique keys
        all_keys = set()
        for personality in personalities:
            all_keys.update(personality.to_dict().keys())
        
        for key in all_keys:
            # Randomly select a personality for this component, weighted by weights
            selected_personality = self._weighted_random_choice(personalities, weights)
            selected_data = selected_personality.to_dict()
            
            if key in selected_data:
                blended[key] = selected_data[key].copy()
        
        return blended
    
    def _blend_persona(self, personalities: List[Personality], weights: BlendWeights) -> Dict[str, Any]:
        """Blend persona information."""
        persona = {
            "name": "Blended Personality",
            "version": "1.0.0",
            "description": "A blended personality",
            "author": "PersonaBlend",
            "tags": [],
            "language": "en",
            "compatibility": []
        }
        
        # Blend compatibility (union of all)
        for personality in personalities:
            persona["compatibility"].extend(personality.persona.compatibility)
        persona["compatibility"] = list(set(persona["compatibility"]))
        
        # Blend tags (weighted by importance)
        for personality in personalities:
            weight = weights.get_weight(personality.persona.name)
            for tag in personality.persona.tags:
                if tag not in persona["tags"]:
                    persona["tags"].append(tag)
        
        return persona
    
    def _blend_core_traits(self, personalities: List[Personality], weights: BlendWeights) -> Dict[str, Any]:
        """Blend core traits using weighted selection."""
        traits = {
            "archetype": "scientist",
            "temperament": "calm",
            "communication_style": "formal"
        }
        
        # Weighted selection for each trait
        for trait in traits.keys():
            trait_values = {}
            for personality in personalities:
                trait_value = getattr(personality.core_traits, trait)
                trait_values[trait_value] = trait_values.get(trait_value, 0) + weights.get_weight(personality.persona.name)
            
            # Select trait with highest weight
            traits[trait] = max(trait_values.keys(), key=lambda k: trait_values[k])
        
        return traits
    
    def _blend_linguistic_profile(self, personalities: List[Personality], weights: BlendWeights) -> Dict[str, Any]:
        """Blend linguistic profile."""
        profile = {
            "tone": [],
            "syntax": "varied",
            "vocabulary": [],
            "fillers": [],
            "punctuation_style": "moderate"
        }
        
        # Blend tones (weighted union)
        tone_weights = {}
        for personality in personalities:
            weight = weights.get_weight(personality.persona.name)
            for tone in personality.linguistic_profile.tone:
                tone_weights[tone] = tone_weights.get(tone, 0) + weight
        
        # Select top tones
        profile["tone"] = sorted(tone_weights.keys(), key=lambda k: tone_weights[k], reverse=True)[:5]
        
        # Blend vocabulary (weighted union)
        vocab_weights = {}
        for personality in personalities:
            weight = weights.get_weight(personality.persona.name)
            for vocab in personality.linguistic_profile.vocabulary:
                vocab_weights[vocab] = vocab_weights.get(vocab, 0) + weight
        
        # Select top vocabulary
        profile["vocabulary"] = sorted(vocab_weights.keys(), key=lambda k: vocab_weights[k], reverse=True)[:15]
        
        # Blend fillers
        filler_weights = {}
        for personality in personalities:
            weight = weights.get_weight(personality.persona.name)
            if personality.linguistic_profile.fillers:
                for filler in personality.linguistic_profile.fillers:
                    filler_weights[filler] = filler_weights.get(filler, 0) + weight
        
        if filler_weights:
            profile["fillers"] = sorted(filler_weights.keys(), key=lambda k: filler_weights[k], reverse=True)[:5]
        
        # Select syntax and punctuation style
        syntax_weights = {}
        punctuation_weights = {}
        for personality in personalities:
            weight = weights.get_weight(personality.persona.name)
            syntax_weights[personality.linguistic_profile.syntax] = syntax_weights.get(personality.linguistic_profile.syntax, 0) + weight
            if personality.linguistic_profile.punctuation_style:
                punctuation_weights[personality.linguistic_profile.punctuation_style] = punctuation_weights.get(personality.linguistic_profile.punctuation_style, 0) + weight
        
        profile["syntax"] = max(syntax_weights.keys(), key=lambda k: syntax_weights[k])
        if punctuation_weights:
            profile["punctuation_style"] = max(punctuation_weights.keys(), key=lambda k: punctuation_weights[k])
        
        return profile
    
    def _blend_behavioral_rules(self, personalities: List[Personality], weights: BlendWeights) -> List[str]:
        """Blend behavioral rules."""
        rules = []
        
        # Collect all rules with weights
        rule_weights = {}
        for personality in personalities:
            weight = weights.get_weight(personality.persona.name)
            for rule in personality.behavioral_rules:
                rule_weights[rule] = rule_weights.get(rule, 0) + weight
        
        # Select top rules
        rules = sorted(rule_weights.keys(), key=lambda k: rule_weights[k], reverse=True)[:10]
        
        return rules
    
    def _blend_trigger_responses(self, personalities: List[Personality], weights: BlendWeights) -> Dict[str, Any]:
        """Blend trigger responses."""
        responses = {}
        
        trigger_types = ["on_greeting", "on_confusion", "on_success", "on_error", "on_goodbye"]
        
        for trigger_type in trigger_types:
            response_weights = {}
            for personality in personalities:
                if personality.trigger_responses:
                    trigger_responses = getattr(personality.trigger_responses, trigger_type, [])
                    if trigger_responses:
                        weight = weights.get_weight(personality.persona.name)
                        for response in trigger_responses:
                            response_weights[response] = response_weights.get(response, 0) + weight
            
            if response_weights:
                responses[trigger_type] = sorted(response_weights.keys(), key=lambda k: response_weights[k], reverse=True)[:3]
        
        return responses
    
    def _blend_advanced_parameters(self, personalities: List[Personality], weights: BlendWeights) -> Dict[str, Any]:
        """Blend advanced parameters using weighted average."""
        params = {}
        
        param_names = ["verbosity", "formality", "humor", "empathy", "creativity", "directness"]
        
        for param_name in param_names:
            weighted_sum = 0
            total_weight = 0
            
            for personality in personalities:
                if personality.advanced_parameters:
                    param_value = getattr(personality.advanced_parameters, param_name)
                    if param_value is not None:
                        weight = weights.get_weight(personality.persona.name)
                        weighted_sum += param_value * weight
                        total_weight += weight
            
            if total_weight > 0:
                params[param_name] = round(weighted_sum / total_weight, 2)
        
        return params
    
    def _blend_safety_guards(self, personalities: List[Personality], weights: BlendWeights) -> Dict[str, Any]:
        """Blend safety guards."""
        guards = {
            "forbidden_topics": [],
            "tone_limits": {},
            "content_filters": []
        }
        
        # Union of forbidden topics
        for personality in personalities:
            if personality.safety_guards and personality.safety_guards.forbidden_topics:
                guards["forbidden_topics"].extend(personality.safety_guards.forbidden_topics)
        
        guards["forbidden_topics"] = list(set(guards["forbidden_topics"]))
        
        # Union of content filters
        for personality in personalities:
            if personality.safety_guards and personality.safety_guards.content_filters:
                guards["content_filters"].extend(personality.safety_guards.content_filters)
        
        guards["content_filters"] = list(set(guards["content_filters"]))
        
        # Average tone limits
        if personalities:
            tone_limits = {"max_aggression": 0, "max_informality": 0}
            for personality in personalities:
                if personality.safety_guards and personality.safety_guards.tone_limits:
                    weight = weights.get_weight(personality.persona.name)
                    for limit_name, limit_value in personality.safety_guards.tone_limits.items():
                        tone_limits[limit_name] = tone_limits.get(limit_name, 0) + limit_value * weight
            
            guards["tone_limits"] = tone_limits
        
        return guards
    
    def _blend_examples(self, personalities: List[Personality], weights: BlendWeights) -> Dict[str, Any]:
        """Blend examples."""
        examples = {"sample_responses": []}
        
        # Collect examples with weights
        example_weights = {}
        for personality in personalities:
            if personality.examples:
                weight = weights.get_weight(personality.persona.name)
                for example in personality.examples.sample_responses:
                    example_key = f"{example.input[:50]}...{example.output[:50]}..."
                    example_weights[example_key] = example_weights.get(example_key, 0) + weight
        
        # Select top examples
        top_examples = sorted(example_weights.keys(), key=lambda k: example_weights[k], reverse=True)[:5]
        
        # Reconstruct examples
        for example_key in top_examples:
            for personality in personalities:
                if personality.examples:
                    for example in personality.examples.sample_responses:
                        if f"{example.input[:50]}...{example.output[:50]}..." == example_key:
                            examples["sample_responses"].append({
                                "input": example.input,
                                "output": example.output,
                                "context": example.context
                            })
                            break
                    else:
                        continue
                    break
        
        return examples
    
    def _blend_metadata(self, personalities: List[Personality], weights: BlendWeights) -> Dict[str, Any]:
        """Blend metadata."""
        from datetime import datetime
        
        metadata = {
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "downloads": 0,
            "rating": 0.0,
            "license": "MIT"
        }
        
        # Average rating
        rating_sum = 0
        rating_count = 0
        for personality in personalities:
            if personality.metadata and personality.metadata.rating is not None:
                weight = weights.get_weight(personality.persona.name)
                rating_sum += personality.metadata.rating * weight
                rating_count += weight
        
        if rating_count > 0:
            metadata["rating"] = round(rating_sum / rating_count, 1)
        
        return metadata
    
    def _blend_component(self, personalities: List[Personality], weights: BlendWeights, component_name: str) -> Any:
        """Blend a specific component."""
        if component_name == "linguistic_profile":
            return self._blend_linguistic_profile(personalities, weights)
        elif component_name == "advanced_parameters":
            return self._blend_advanced_parameters(personalities, weights)
        elif component_name == "safety_guards":
            return self._blend_safety_guards(personalities, weights)
        else:
            return {}
    
    def _weighted_random_choice(self, personalities: List[Personality], weights: BlendWeights) -> Personality:
        """Choose a personality weighted by importance."""
        choices = list(personalities)
        weights_list = [weights.get_weight(p.persona.name) for p in personalities]
        return random.choices(choices, weights=weights_list)[0]
    
    def _generate_blend_name(self, personalities: List[Personality], weights: BlendWeights) -> str:
        """Generate a name for the blended personality."""
        dominant_name = max(weights.weights.keys(), key=lambda k: weights.weights[k])
        return f"Blend of {dominant_name}"
    
    def _generate_blend_description(self, personalities: List[Personality], weights: BlendWeights) -> str:
        """Generate a description for the blended personality."""
        names = list(weights.weights.keys())
        if len(names) == 2:
            return f"A unique blend of {names[0]} and {names[1]} personalities."
        else:
            return f"A carefully crafted blend of {len(names)} distinct personalities."
    
    def _blend_tags(self, personalities: List[Personality], weights: BlendWeights) -> List[str]:
        """Blend tags from all personalities."""
        all_tags = []
        for personality in personalities:
            all_tags.extend(personality.persona.tags)
        
        # Remove duplicates and add blend tag
        unique_tags = list(set(all_tags))
        unique_tags.append("blended")
        
        return unique_tags[:10]  # Limit to 10 tags
    
    def _merge_dicts(self, dict1: Dict[str, Any], dict2: Dict[str, Any], merge_weight: float) -> Dict[str, Any]:
        """Merge two dictionaries with specified weight."""
        result = dict1.copy()
        
        for key, value in dict2.items():
            if key in result:
                if isinstance(value, dict) and isinstance(result[key], dict):
                    result[key] = self._merge_dicts(result[key], value, merge_weight)
                elif isinstance(value, (int, float)) and isinstance(result[key], (int, float)):
                    result[key] = result[key] * (1 - merge_weight) + value * merge_weight
            else:
                result[key] = value
        
        return result
