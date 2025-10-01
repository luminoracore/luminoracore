"""Personality blender for LuminoraCore CLI."""

import json
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime

from luminoracore_cli.utils.errors import CLIError


class PersonalityBlender:
    """Blends multiple personalities with custom weights."""
    
    def __init__(self):
        """Initialize the blender."""
        pass
    
    def blend(
        self,
        personalities: List[Tuple[Dict[str, Any], float]],
        custom_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Blend multiple personalities with custom weights.
        
        Args:
            personalities: List of (personality_data, weight) tuples
            custom_name: Custom name for blended personality
        
        Returns:
            Blended personality data
        """
        try:
            # Validate inputs
            if not personalities:
                raise CLIError("No personalities provided for blending")
            
            if len(personalities) < 2:
                raise CLIError("At least 2 personalities required for blending")
            
            # Validate weights
            total_weight = sum(weight for _, weight in personalities)
            if abs(total_weight - 1.0) > 0.01:
                raise CLIError("Personality weights must sum to 1.0")
            
            # Start with base structure
            blended = {
                "persona": {},
                "core_traits": {},
                "linguistic_profile": {},
                "behavioral_rules": [],
                "advanced_parameters": {}
            }
            
            # Blend persona information
            blended["persona"] = self._blend_persona(personalities, custom_name)
            
            # Blend core traits
            blended["core_traits"] = self._blend_core_traits(personalities)
            
            # Blend linguistic profile
            blended["linguistic_profile"] = self._blend_linguistic_profile(personalities)
            
            # Blend behavioral rules
            blended["behavioral_rules"] = self._blend_behavioral_rules(personalities)
            
            # Blend advanced parameters
            blended["advanced_parameters"] = self._blend_advanced_parameters(personalities)
            
            # Add blending metadata
            blended["blending_metadata"] = {
                "blended_at": datetime.now().isoformat(),
                "source_personalities": [
                    {
                        "name": p[0].get("persona", {}).get("name", "Unknown"),
                        "weight": p[1]
                    }
                    for p in personalities
                ],
                "blending_method": "weighted_average"
            }
            
            return blended
            
        except Exception as e:
            raise CLIError(f"Personality blending failed: {e}")
    
    def _blend_persona(self, personalities: List[Tuple[Dict[str, Any], float]], custom_name: Optional[str] = None) -> Dict[str, Any]:
        """Blend persona information."""
        persona = {}
        
        # Use custom name or create one
        if custom_name:
            persona["name"] = custom_name
        else:
            # Create name from source personalities
            names = [p[0].get("persona", {}).get("name", "Unknown") for p in personalities]
            persona["name"] = f"Blended: {' + '.join(names[:3])}"
        
        # Blend description
        descriptions = []
        for p_data, weight in personalities:
            desc = p_data.get("persona", {}).get("description", "")
            if desc:
                descriptions.append(desc)
        
        if descriptions:
            persona["description"] = "A blended personality combining: " + "; ".join(descriptions[:2])
        else:
            persona["description"] = "A blended personality created from multiple sources"
        
        # Blend archetype (use most common)
        archetypes = {}
        for p_data, weight in personalities:
            arch = p_data.get("persona", {}).get("archetype", "unknown")
            archetypes[arch] = archetypes.get(arch, 0) + weight
        
        persona["archetype"] = max(archetypes.items(), key=lambda x: x[1])[0]
        
        # Blend version
        persona["version"] = "1.0.0"
        
        # Blend author
        authors = set()
        for p_data, _ in personalities:
            author = p_data.get("persona", {}).get("author", "")
            if author:
                authors.add(author)
        
        if authors:
            persona["author"] = ", ".join(sorted(authors))
        else:
            persona["author"] = "Blended Personality"
        
        # Blend tags
        all_tags = set()
        for p_data, _ in personalities:
            tags = p_data.get("persona", {}).get("tags", [])
            all_tags.update(tags)
        
        persona["tags"] = list(all_tags) + ["blended"]
        
        return persona
    
    def _blend_core_traits(self, personalities: List[Tuple[Dict[str, Any], float]]) -> Dict[str, Any]:
        """Blend core traits."""
        traits = {}
        
        # Blend archetype (use most common)
        archetypes = {}
        for p_data, weight in personalities:
            arch = p_data.get("core_traits", {}).get("archetype", "unknown")
            archetypes[arch] = archetypes.get(arch, 0) + weight
        
        traits["archetype"] = max(archetypes.items(), key=lambda x: x[1])[0]
        
        # Blend temperament (use most common)
        temperaments = {}
        for p_data, weight in personalities:
            temp = p_data.get("core_traits", {}).get("temperament", "unknown")
            temperaments[temp] = temperaments.get(temp, 0) + weight
        
        traits["temperament"] = max(temperaments.items(), key=lambda x: x[1])[0]
        
        # Blend communication style (use most common)
        comm_styles = {}
        for p_data, weight in personalities:
            style = p_data.get("core_traits", {}).get("communication_style", "unknown")
            comm_styles[style] = comm_styles.get(style, 0) + weight
        
        traits["communication_style"] = max(comm_styles.items(), key=lambda x: x[1])[0]
        
        # Blend values (weighted union)
        all_values = {}
        for p_data, weight in personalities:
            values = p_data.get("core_traits", {}).get("values", [])
            for value in values:
                all_values[value] = all_values.get(value, 0) + weight
        
        # Take top values
        traits["values"] = sorted(all_values.items(), key=lambda x: x[1], reverse=True)[:5]
        traits["values"] = [v[0] for v in traits["values"]]
        
        # Blend motivations (weighted union)
        all_motivations = {}
        for p_data, weight in personalities:
            motivations = p_data.get("core_traits", {}).get("motivations", [])
            for motivation in motivations:
                all_motivations[motivation] = all_motivations.get(motivation, 0) + weight
        
        # Take top motivations
        traits["motivations"] = sorted(all_motivations.items(), key=lambda x: x[1], reverse=True)[:5]
        traits["motivations"] = [m[0] for m in traits["motivations"]]
        
        return traits
    
    def _blend_linguistic_profile(self, personalities: List[Tuple[Dict[str, Any], float]]) -> Dict[str, Any]:
        """Blend linguistic profile."""
        profile = {}
        
        # Blend tone (weighted union)
        all_tones = {}
        for p_data, weight in personalities:
            tones = p_data.get("linguistic_profile", {}).get("tone", [])
            for tone in tones:
                all_tones[tone] = all_tones.get(tone, 0) + weight
        
        # Take top tones
        profile["tone"] = sorted(all_tones.items(), key=lambda x: x[1], reverse=True)[:5]
        profile["tone"] = [t[0] for t in profile["tone"]]
        
        # Blend vocabulary (weighted union)
        all_vocabulary = {}
        for p_data, weight in personalities:
            vocab = p_data.get("linguistic_profile", {}).get("vocabulary", [])
            for word in vocab:
                all_vocabulary[word] = all_vocabulary.get(word, 0) + weight
        
        # Take top vocabulary
        profile["vocabulary"] = sorted(all_vocabulary.items(), key=lambda x: x[1], reverse=True)[:10]
        profile["vocabulary"] = [v[0] for v in profile["vocabulary"]]
        
        # Blend speech patterns (weighted union)
        all_patterns = {}
        for p_data, weight in personalities:
            patterns = p_data.get("linguistic_profile", {}).get("speech_patterns", [])
            for pattern in patterns:
                all_patterns[pattern] = all_patterns.get(pattern, 0) + weight
        
        # Take top patterns
        profile["speech_patterns"] = sorted(all_patterns.items(), key=lambda x: x[1], reverse=True)[:5]
        profile["speech_patterns"] = [p[0] for p in profile["speech_patterns"]]
        
        # Blend formality level (weighted average)
        formality_levels = {"casual": 1, "professional": 2, "formal": 3}
        weighted_formality = 0
        total_weight = 0
        
        for p_data, weight in personalities:
            formality = p_data.get("linguistic_profile", {}).get("formality_level", "casual")
            if formality in formality_levels:
                weighted_formality += formality_levels[formality] * weight
                total_weight += weight
        
        if total_weight > 0:
            avg_formality = weighted_formality / total_weight
            if avg_formality <= 1.5:
                profile["formality_level"] = "casual"
            elif avg_formality <= 2.5:
                profile["formality_level"] = "professional"
            else:
                profile["formality_level"] = "formal"
        else:
            profile["formality_level"] = "casual"
        
        # Blend response length (weighted average)
        response_lengths = {"short": 1, "moderate": 2, "detailed": 3}
        weighted_length = 0
        total_weight = 0
        
        for p_data, weight in personalities:
            length = p_data.get("linguistic_profile", {}).get("response_length", "moderate")
            if length in response_lengths:
                weighted_length += response_lengths[length] * weight
                total_weight += weight
        
        if total_weight > 0:
            avg_length = weighted_length / total_weight
            if avg_length <= 1.5:
                profile["response_length"] = "short"
            elif avg_length <= 2.5:
                profile["response_length"] = "moderate"
            else:
                profile["response_length"] = "detailed"
        else:
            profile["response_length"] = "moderate"
        
        return profile
    
    def _blend_behavioral_rules(self, personalities: List[Tuple[Dict[str, Any], float]]) -> List[str]:
        """Blend behavioral rules."""
        all_rules = {}
        
        for p_data, weight in personalities:
            rules = p_data.get("behavioral_rules", [])
            for rule in rules:
                all_rules[rule] = all_rules.get(rule, 0) + weight
        
        # Take top rules
        sorted_rules = sorted(all_rules.items(), key=lambda x: x[1], reverse=True)
        return [rule[0] for rule in sorted_rules[:10]]
    
    def _blend_advanced_parameters(self, personalities: List[Tuple[Dict[str, Any], float]]) -> Dict[str, Any]:
        """Blend advanced parameters."""
        params = {}
        
        # Blend temperature (weighted average)
        weighted_temp = 0
        total_weight = 0
        
        for p_data, weight in personalities:
            temp = p_data.get("advanced_parameters", {}).get("temperature", 0.7)
            weighted_temp += temp * weight
            total_weight += weight
        
        if total_weight > 0:
            params["temperature"] = weighted_temp / total_weight
        else:
            params["temperature"] = 0.7
        
        # Blend top_p (weighted average)
        weighted_top_p = 0
        total_weight = 0
        
        for p_data, weight in personalities:
            top_p = p_data.get("advanced_parameters", {}).get("top_p", 0.9)
            weighted_top_p += top_p * weight
            total_weight += weight
        
        if total_weight > 0:
            params["top_p"] = weighted_top_p / total_weight
        else:
            params["top_p"] = 0.9
        
        # Blend max_tokens (weighted average)
        weighted_max_tokens = 0
        total_weight = 0
        
        for p_data, weight in personalities:
            max_tokens = p_data.get("advanced_parameters", {}).get("max_tokens", 500)
            weighted_max_tokens += max_tokens * weight
            total_weight += weight
        
        if total_weight > 0:
            params["max_tokens"] = int(weighted_max_tokens / total_weight)
        else:
            params["max_tokens"] = 500
        
        # Blend frequency_penalty (weighted average)
        weighted_freq_penalty = 0
        total_weight = 0
        
        for p_data, weight in personalities:
            freq_penalty = p_data.get("advanced_parameters", {}).get("frequency_penalty", 0.0)
            weighted_freq_penalty += freq_penalty * weight
            total_weight += weight
        
        if total_weight > 0:
            params["frequency_penalty"] = weighted_freq_penalty / total_weight
        else:
            params["frequency_penalty"] = 0.0
        
        # Blend presence_penalty (weighted average)
        weighted_pres_penalty = 0
        total_weight = 0
        
        for p_data, weight in personalities:
            pres_penalty = p_data.get("advanced_parameters", {}).get("presence_penalty", 0.0)
            weighted_pres_penalty += pres_penalty * weight
            total_weight += weight
        
        if total_weight > 0:
            params["presence_penalty"] = weighted_pres_penalty / total_weight
        else:
            params["presence_penalty"] = 0.0
        
        return params
