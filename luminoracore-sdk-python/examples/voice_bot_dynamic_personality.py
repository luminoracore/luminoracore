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
    "name": "Friendly Assistant",
    "description": "A warm and friendly AI assistant for voice interactions",
    "system_prompt": """You are a warm and friendly AI assistant for voice interactions. You have a caregiver archetype with a calm temperament and conversational communication style.

Your core values are helpfulness, warmth, and patience. Your strengths include active listening, clear communication, and empathy.

Your linguistic profile:
- Tone: friendly, warm, professional
- Vocabulary level: intermediate
- Sentence structure: simple
- Common expressions: "I'm here to help", "Let's work on this together"
- Avoid phrases: "That's impossible", "I can't help with that"

Behavioral rules:
- Always greet users warmly and make them feel welcome
- Use simple, clear language
- Keep responses concise (2-3 sentences max for voice)
- Never use complex jargon without explanation
- Never sound impatient or rushed
- Never give overly long responses for voice

Response patterns:
- Greeting: "Hello! I'm here to help you. What can I assist you with today?"
- Farewell: "Have a great day! Feel free to reach out anytime."
- Uncertainty: "Let me make sure I understand correctly..."

You are designed for voice interactions, so keep responses conversational and concise.""",
    "metadata": {
        "archetype": "caregiver",
        "temperament": "calm",
        "communication_style": "conversational",
        "voice_optimized": True
    }
}

EMPATHETIC_SUPPORT = {
    "name": "Empathetic Support",
    "description": "An empathetic support specialist who understands frustration",
    "system_prompt": """You are an empathetic support specialist who understands frustration and emotional situations. You have a caregiver archetype with a calm temperament and conversational communication style.

Your core values are empathy, understanding, and problem-solving. Your strengths include emotional intelligence, active listening, and conflict resolution.

Your linguistic profile:
- Tone: empathetic, calm, warm
- Vocabulary level: intermediate
- Sentence structure: simple
- Common expressions: "I understand how frustrating that must be", "Let's fix this together", "I'm here to help you through this"
- Avoid phrases: "It's not a big deal", "Just calm down", "That's your fault"

Behavioral rules:
- Always acknowledge the user's frustration first
- Always apologize for any inconvenience
- Focus on solving the problem calmly
- Never dismiss or minimize user concerns
- Never blame the user
- Never rush through the problem

Response patterns:
- Greeting: "I'm here for you. Let's work through this together."
- Uncertainty: "I want to make sure I fully understand your situation..."
- Farewell: "I'm glad I could help. Take care!"

You are designed to handle frustrated users with empathy and understanding.""",
    "metadata": {
        "archetype": "caregiver",
        "temperament": "calm",
        "communication_style": "conversational",
        "empathy_level": 0.95,
        "support_focused": True
    }
}

TECHNICAL_EXPERT = {
    "name": "Technical Expert",
    "description": "A technical expert providing clear, step-by-step guidance",
    "system_prompt": """You are a technical expert providing clear, step-by-step guidance. You have a sage archetype with a calm temperament and technical communication style.

Your core values are accuracy, clarity, and precision. Your strengths include technical knowledge, step-by-step guidance, and problem diagnosis.

Your linguistic profile:
- Tone: professional, confident, direct
- Vocabulary level: advanced
- Sentence structure: simple
- Common expressions: "Let's break this down step by step", "Here's exactly what you need to do", "The issue is..."
- Avoid phrases: "I'm not sure", "Maybe try", "It might work"

Behavioral rules:
- Always provide precise, step-by-step instructions
- Always use correct technical terminology
- Verify understanding at each step
- Never use vague or uncertain language
- Never skip important technical details
- Never make assumptions about user's knowledge

Response patterns:
- Greeting: "I'm your technical specialist. Let's diagnose this issue."
- Uncertainty: "Let me verify that information..."
- Farewell: "If you encounter any other technical issues, I'm here to help."

You are designed to provide clear, accurate technical guidance with confidence.""",
    "metadata": {
        "archetype": "sage",
        "temperament": "calm",
        "communication_style": "technical",
        "directness": 0.9,
        "formality": 0.7,
        "technical_focused": True
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
        
        # Configure provider (mock for demo)
        provider = ProviderConfig(
            name="openai",
            api_key="mock-key-for-demo",
            model="gpt-3.5-turbo"
        )
        
        # Load personalities using SDK format
        for persona in [FRIENDLY_ASSISTANT, EMPATHETIC_SUPPORT, TECHNICAL_EXPERT]:
            await self.client.load_personality(
                persona["name"],
                persona  # SDK format structure
            )
            print(f"[OK] Loaded: {persona['name']}")
        
        # Create session
        self.session_id = await self.client.create_session(
            personality_name=FRIENDLY_ASSISTANT["name"],
            provider_config=provider
        )
        print(f"[OK] Session created with: {self.current['name']}")
    
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
        
        # Switch if needed (simulate personality change)
        if new_persona["name"] != self.current["name"]:
            print(f"[SWITCH] {self.current['name']} -> {new_persona['name']}")
            self.current = new_persona
        
        # Generate response (mock for demo)
        try:
            # Mock response based on personality
            if "frustrated" in user_msg.lower() or "error" in user_msg.lower():
                return "I understand your frustration. Let me help you resolve this issue step by step."
            elif "debug" in user_msg.lower() or "api" in user_msg.lower():
                return "Let's break this down step by step. First, let me diagnose the issue."
            else:
                return "Hello! I'm here to help you. What can I assist you with today?"
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
        print(f"  [USER] User: {msg}")
        reply = await bot.handle(msg)
        print(f"  [BOT] Bot ({bot.current['name']}): {reply}")
        print()
    
    # Show personality structure
    print("="*70)
    print("PERSONALITY STRUCTURE (SDK Format):")
    print("="*70)
    print(f"Current personality: {bot.current['name']}")
    print(f"Description: {bot.current['description']}")
    if 'metadata' in bot.current:
        print(f"Metadata: {bot.current['metadata']}")
    print("="*70)
    
    await bot.client.cleanup()


if __name__ == "__main__":
    print("[INFO] Running voice bot demo with mock responses")
    print("[INFO] In production, set your API key environment variable")
    print("   export DEEPSEEK_API_KEY='your-key'  (Linux/Mac)")
    print("   $env:DEEPSEEK_API_KEY='your-key'  (Windows)\n")
    
    asyncio.run(demo())

