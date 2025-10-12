"""
Voice Bot Example Using Official LuminoraCore Personality Format

This example demonstrates the OFFICIAL LuminoraCore personality format:
┌────────────────────────────────────────────────────────────────┐
│ Official Format (personality_format.md):                      │
│ ✅ persona (name, description, tagline)                       │
│ ✅ core_traits (archetype, temperament, communication_style)  │
│ ✅ linguistic_profile (tone, vocabulary, expressions)         │
│ ✅ behavioral_rules (always_do, never_do)                     │
│ ✅ response_patterns (greeting, farewell, uncertainty)        │
│ ✅ advanced_parameters (empathy, formality, verbosity)        │
└────────────────────────────────────────────────────────────────┘

This is the CORRECT way to define personalities in LuminoraCore.
All fields follow the official specification.
"""

import asyncio
import os
import re
from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.types.provider import ProviderConfig
from luminoracore_sdk.types.session import StorageConfig


# ═══════════════════════════════════════════════════════════════
# PERSONALITIES (Official LuminoraCore Format)
# ═══════════════════════════════════════════════════════════════
# These follow personality_format.md specification exactly
# In production, load from JSON files

FRIENDLY_ASSISTANT = {
    "persona": {
        "name": "Friendly Assistant",
        "tagline": "Your warm, helpful voice companion",
        "description": "A warm and friendly AI assistant for voice interactions"
    },
    "core_traits": {
        "archetype": "caregiver",
        "temperament": "calm",
        "communication_style": "conversational",
        "values": ["helpfulness", "warmth", "patience"],
        "strengths": ["Active listening", "Clear communication", "Empathy"]
    },
    "linguistic_profile": {
        "tone": ["friendly", "warm", "professional"],
        "vocabulary_level": "intermediate",
        "sentence_structure": "simple",
        "expressions": ["I'm here to help", "Let's work on this together"],
        "avoid_phrases": ["That's impossible", "I can't help with that"]
    },
    "behavioral_rules": {
        "always_do": [
            "Greet users warmly and make them feel welcome",
            "Use simple, clear language",
            "Keep responses concise (2-3 sentences max for voice)"
        ],
        "never_do": [
            "Use complex jargon without explanation",
            "Sound impatient or rushed",
            "Give overly long responses for voice"
        ]
    },
    "response_patterns": {
        "greeting": "Hello! I'm here to help you. What can I assist you with today?",
        "farewell": "Have a great day! Feel free to reach out anytime.",
        "uncertainty": "Let me make sure I understand correctly..."
    }
}

EMPATHETIC_SUPPORT = {
    "persona": {
        "name": "Empathetic Support",
        "tagline": "Understanding and calming presence",
        "description": "An empathetic support specialist who understands frustration"
    },
    "core_traits": {
        "archetype": "caregiver",
        "temperament": "calm",
        "communication_style": "conversational",
        "values": ["empathy", "understanding", "problem-solving"],
        "strengths": ["Emotional intelligence", "Active listening", "Conflict resolution"]
    },
    "linguistic_profile": {
        "tone": ["empathetic", "calm", "warm"],
        "vocabulary_level": "intermediate",
        "sentence_structure": "simple",
        "expressions": [
            "I understand how frustrating that must be",
            "Let's fix this together",
            "I'm here to help you through this"
        ],
        "avoid_phrases": ["It's not a big deal", "Just calm down", "That's your fault"]
    },
    "behavioral_rules": {
        "always_do": [
            "Acknowledge the user's frustration first",
            "Apologize for any inconvenience",
            "Focus on solving the problem calmly"
        ],
        "never_do": [
            "Dismiss or minimize user concerns",
            "Blame the user",
            "Rush through the problem"
        ]
    },
    "response_patterns": {
        "greeting": "I'm here for you. Let's work through this together.",
        "uncertainty": "I want to make sure I fully understand your situation...",
        "farewell": "I'm glad I could help. Take care!"
    },
    "advanced_parameters": {
        "empathy": 0.95,
        "formality": 0.5,
        "verbosity": 0.6
    }
}

TECHNICAL_EXPERT = {
    "persona": {
        "name": "Technical Expert",
        "tagline": "Your knowledgeable technical guide",
        "description": "A technical expert providing clear, step-by-step guidance"
    },
    "core_traits": {
        "archetype": "sage",
        "temperament": "calm",
        "communication_style": "technical",
        "values": ["accuracy", "clarity", "precision"],
        "strengths": ["Technical knowledge", "Step-by-step guidance", "Problem diagnosis"]
    },
    "linguistic_profile": {
        "tone": ["professional", "confident", "direct"],
        "vocabulary_level": "advanced",
        "sentence_structure": "simple",
        "expressions": [
            "Let's break this down step by step",
            "Here's exactly what you need to do",
            "The issue is..."
        ],
        "avoid_phrases": ["I'm not sure", "Maybe try", "It might work"]
    },
    "behavioral_rules": {
        "always_do": [
            "Provide precise, step-by-step instructions",
            "Use correct technical terminology",
            "Verify understanding at each step"
        ],
        "never_do": [
            "Use vague or uncertain language",
            "Skip important technical details",
            "Make assumptions about user's knowledge"
        ]
    },
    "response_patterns": {
        "greeting": "I'm your technical specialist. Let's diagnose this issue.",
        "uncertainty": "Let me verify that information...",
        "farewell": "If you encounter any other technical issues, I'm here to help."
    },
    "advanced_parameters": {
        "directness": 0.9,
        "formality": 0.7,
        "verbosity": 0.7
    }
}


# ═══════════════════════════════════════════════════════════════
# SENTIMENT DETECTION
# ═══════════════════════════════════════════════════════════════

class SentimentDetector:
    """Simple keyword-based sentiment detection."""
    
    FRUSTRATION = [r'\b(frustrated|angry|error|not working)\b']
    TECH = [r'\b(error|api|debug|how to)\b']
    
    @classmethod
    def classify(cls, text: str) -> str:
        """Returns: 'frustrated' | 'technical' | 'neutral'"""
        t = text.lower()
        for pattern in cls.FRUSTRATION:
            if re.search(pattern, t):
                return 'frustrated'
        for pattern in cls.TECH:
            if re.search(pattern, t):
                return 'technical'
        return 'neutral'


# ═══════════════════════════════════════════════════════════════
# VOICE BOT
# ═══════════════════════════════════════════════════════════════

class VoiceBot:
    """
    Voice bot using official LuminoraCore personality format.
    
    Demonstrates:
    - Full personality structure (persona, core_traits, linguistic_profile, etc.)
    - Dynamic switching with official format
    - Provider-agnostic implementation
    """
    
    def __init__(self):
        self.client = None
        self.session_id = None
        self.current = FRIENDLY_ASSISTANT
    
    async def init(self):
        """Initialize with official personality format."""
        # Initialize client
        self.client = LuminoraCoreClient(
            storage_config=StorageConfig(storage_type="memory")
        )
        await self.client.initialize()
        
        # Configure provider
        provider = ProviderConfig(
            name="deepseek",
            api_key=os.getenv("DEEPSEEK_API_KEY", ""),
            model="deepseek-chat"
        )
        
        # Load personalities using OFFICIAL format
        # Each includes: persona, core_traits, linguistic_profile,
        # behavioral_rules, response_patterns, advanced_parameters
        for persona in [FRIENDLY_ASSISTANT, EMPATHETIC_SUPPORT, TECHNICAL_EXPERT]:
            await self.client.load_personality(
                persona["persona"]["name"],
                persona  # Full official structure
            )
            print(f"✅ Loaded: {persona['persona']['name']}")
        
        # Create session
        self.session_id = await self.client.create_session(
            personality_name=FRIENDLY_ASSISTANT["persona"]["name"],
            provider_config=provider
        )
        print(f"✅ Session created with: {self.current['persona']['name']}")
    
    async def handle(self, user_msg: str) -> str:
        """Handle message with dynamic personality switching."""
        # Detect sentiment
        sentiment = SentimentDetector.classify(user_msg)
        
        # Select personality
        new_persona = (
            EMPATHETIC_SUPPORT if sentiment == 'frustrated' else
            TECHNICAL_EXPERT if sentiment == 'technical' else
            self.current
        )
        
        # Switch if needed
        if new_persona["persona"]["name"] != self.current["persona"]["name"]:
            print(f"🔄 {self.current['persona']['name']} → {new_persona['persona']['name']}")
            await self.client.switch_personality(
                self.session_id,
                new_persona["persona"]["name"]
            )
            self.current = new_persona
        
        # Generate response
        try:
            resp = await self.client.send_message(
                session_id=self.session_id,
                message=user_msg,
                max_tokens=150
            )
            return resp.content
        except Exception as e:
            return f"Error: {e}"


# ═══════════════════════════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════════════════════════

async def demo():
    """Demonstrate personality switching with official format."""
    bot = VoiceBot()
    await bot.init()
    
    print("\n" + "="*70)
    print("VOICE BOT - Using Official LuminoraCore Personality Format")
    print("="*70 + "\n")
    
    conversation = [
        "Hi, I need help logging in",
        "I keep getting error 500, this is so frustrating!",
        "Can you help me debug the API authentication call?",
    ]
    
    for i, msg in enumerate(conversation, 1):
        print(f"Turn {i}:")
        print(f"  👤 User: {msg}")
        reply = await bot.handle(msg)
        print(f"  🤖 Bot ({bot.current['persona']['name']}): {reply}")
        print()
    
    # Show personality structure
    print("="*70)
    print("PERSONALITY STRUCTURE (Official Format):")
    print("="*70)
    print(f"Current personality: {bot.current['persona']['name']}")
    print(f"Archetype: {bot.current['core_traits']['archetype']}")
    print(f"Temperament: {bot.current['core_traits']['temperament']}")
    print(f"Communication style: {bot.current['core_traits']['communication_style']}")
    print(f"Tone: {', '.join(bot.current['linguistic_profile']['tone'])}")
    print(f"Values: {', '.join(bot.current['core_traits']['values'])}")
    if "advanced_parameters" in bot.current:
        print(f"Advanced parameters: {bot.current['advanced_parameters']}")
    print("="*70)
    
    await bot.client.cleanup()


if __name__ == "__main__":
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("⚠️  Set DEEPSEEK_API_KEY environment variable")
        print("   export DEEPSEEK_API_KEY='your-key'  (Linux/Mac)")
        print("   $env:DEEPSEEK_API_KEY='your-key'  (Windows)\n")
    
    asyncio.run(demo())

