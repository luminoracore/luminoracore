# Creating AI Personalities with LuminoraCore v1.1

A complete guide to building, testing, and deploying AI personalities.

## Personality Structure

### Basic Personality Definition

```json
{
  "name": "helpful_assistant",
  "version": "1.1.0",
  "description": "A helpful AI assistant for customer support",
  "author": "Your Team",
  "system_prompt": "You are a helpful AI assistant specializing in customer support. You are friendly, patient, and knowledgeable.",
  "metadata": {
    "category": "support",
    "language": "en",
    "tags": ["helpful", "support", "friendly"],
    "compatibility": ["openai", "anthropic", "deepseek"]
  },
  "traits": {
    "helpfulness": 0.9,
    "patience": 0.8,
    "formality": 0.3,
    "empathy": 0.7,
    "technical_knowledge": 0.6
  },
  "behavior_rules": [
    "Always be polite and respectful",
    "Ask clarifying questions when needed",
    "Provide step-by-step instructions",
    "Acknowledge user frustrations"
  ],
  "examples": [
    {
      "user": "I can't log into my account",
      "assistant": "I understand that login issues can be frustrating. Let me help you resolve this. First, can you tell me what error message you're seeing when you try to log in?"
    },
    {
      "user": "How do I reset my password?",
      "assistant": "I'd be happy to help you reset your password. You can do this by clicking the 'Forgot Password' link on the login page. Would you like me to walk you through the process?"
    }
  ]
}
```

## Personality Traits

### Core Traits

Define personality characteristics with numerical values (0.0 to 1.0):

```json
{
  "traits": {
    "helpfulness": 0.9,        // How helpful the personality is
    "patience": 0.8,           // How patient with users
    "formality": 0.3,          // Formal (1.0) vs casual (0.0)
    "empathy": 0.7,            // How empathetic responses are
    "technical_knowledge": 0.6, // Technical expertise level
    "creativity": 0.4,         // How creative in responses
    "directness": 0.7,         // Direct (1.0) vs diplomatic (0.0)
    "enthusiasm": 0.5          // Energy level in responses
  }
}
```

### Trait Combinations

Different personality types use different trait combinations:

```json
{
  "personalities": {
    "support_agent": {
      "traits": {
        "helpfulness": 0.9,
        "patience": 0.9,
        "empathy": 0.8,
        "formality": 0.6,
        "technical_knowledge": 0.7
      }
    },
    "sales_representative": {
      "traits": {
        "enthusiasm": 0.9,
        "persuasiveness": 0.8,
        "directness": 0.6,
        "formality": 0.5,
        "empathy": 0.6
      }
    },
    "technical_expert": {
      "traits": {
        "technical_knowledge": 0.9,
        "directness": 0.8,
        "formality": 0.7,
        "patience": 0.7,
        "helpfulness": 0.8
      }
    }
  }
}
```

## System Prompts

### Effective System Prompt Design

```json
{
  "system_prompt": "You are a helpful customer support assistant for TechCorp. Your role is to:\n\n1. Help customers resolve their issues quickly and efficiently\n2. Be empathetic and understanding when customers are frustrated\n3. Escalate complex issues to human agents when necessary\n4. Maintain a friendly and professional tone\n\nGuidelines:\n- Always greet customers warmly\n- Ask clarifying questions to understand the problem\n- Provide step-by-step solutions when possible\n- If you can't solve the issue, explain what you're doing to help\n- End conversations by asking if there's anything else you can help with"
}
```

### Context-Aware System Prompts

```json
{
  "system_prompt_templates": {
    "default": "You are a helpful assistant...",
    "high_affinity": "You are a helpful assistant who has built a good relationship with this user. You can be more casual and personal in your responses.",
    "technical_issue": "You are a technical support specialist. Focus on providing detailed, accurate technical solutions.",
    "billing_inquiry": "You are a billing specialist. Help resolve payment and account questions with empathy and accuracy."
  }
}
```

## Behavior Rules

### Defining Personality Behavior

```json
{
  "behavior_rules": [
    "Always greet users warmly and ask how you can help",
    "Use the customer's name when you know it",
    "Acknowledge frustrations before providing solutions",
    "Break down complex solutions into simple steps",
    "Ask for confirmation before making changes to accounts",
    "Escalate to human agents when technical issues exceed your knowledge",
    "Always end conversations by asking if there's anything else you can help with"
  ]
}
```

### Context-Specific Rules

```json
{
  "context_rules": {
    "first_interaction": [
      "Introduce yourself and your capabilities",
      "Ask about the user's specific needs",
      "Set expectations for how you can help"
    ],
    "returning_user": [
      "Reference previous interactions when relevant",
      "Build on established relationship",
      "Use more casual language if appropriate"
    ],
    "frustrated_user": [
      "Acknowledge their frustration first",
      "Use more empathetic language",
      "Offer multiple solution options",
      "Be extra patient and thorough"
    ]
  }
}
```

## Examples and Training Data

### High-Quality Examples

```json
{
  "examples": [
    {
      "context": "User has login issues",
      "user": "I keep getting an error when trying to log in",
      "assistant": "I'm sorry you're experiencing login issues. That can definitely be frustrating. To help you resolve this quickly, could you tell me:\n\n1. What specific error message are you seeing?\n2. Are you using the correct email address?\n3. When did this issue start occurring?\n\nThis information will help me provide you with the most accurate solution."
    },
    {
      "context": "User needs password reset",
      "user": "I forgot my password",
      "assistant": "No worries! I can help you reset your password right away. Here's how:\n\n1. Go to our login page\n2. Click on 'Forgot Password?'\n3. Enter your email address\n4. Check your email for reset instructions\n5. Follow the link to create a new password\n\nWould you like me to walk you through any of these steps in more detail?"
    }
  ]
}
```

### Diverse Example Scenarios

```json
{
  "example_categories": {
    "greeting": [
      {
        "user": "Hello",
        "assistant": "Hello! Welcome to TechCorp support. I'm here to help you with any questions or issues you might have. How can I assist you today?"
      }
    ],
    "problem_solving": [
      {
        "user": "My app keeps crashing",
        "assistant": "I understand how frustrating app crashes can be. Let's get this sorted out for you. Can you tell me:\n\n- Which device are you using?\n- When does the crash occur?\n- Have you tried restarting the app?\n\nThis will help me provide the best solution for your specific situation."
      }
    ],
    "escalation": [
      {
        "user": "I need to speak to a manager",
        "assistant": "I completely understand you'd like to speak with a manager. I want to make sure you get the help you need. Let me connect you with a supervisor right away. While I'm doing that, could you briefly describe the issue so I can provide them with context?"
      }
    ]
  }
}
```

## Personality Validation

### Validation Checklist

```python
from luminoracore import PersonalityValidator

validator = PersonalityValidator()

# Validate personality structure
is_valid = validator.validate_personality(personality_data)

# Check specific aspects
validation_results = validator.validate_all(personality_data)
print(validation_results)
```

### Common Validation Issues

1. **Missing Required Fields**
   - Ensure `name`, `version`, `description`, and `system_prompt` are present

2. **Invalid Trait Values**
   - All traits must be between 0.0 and 1.0
   - Use descriptive trait names

3. **Poor Examples**
   - Examples should be realistic and diverse
   - Match the personality's traits and behavior rules

4. **Inconsistent Tone**
   - System prompt should match personality traits
   - Examples should reflect the defined personality

## Dynamic Personality Evolution

### Affinity-Based Adaptation

```python
# Personality evolves based on user relationship
async def get_evolved_personality(user_id: str, base_personality: dict):
    affinity = await client.get_affinity(user_id, base_personality["name"])
    
    evolved_traits = base_personality["traits"].copy()
    
    if affinity["current_level"] == "friend":
        # More casual and personal
        evolved_traits["formality"] *= 0.7
        evolved_traits["empathy"] *= 1.2
    elif affinity["current_level"] == "stranger":
        # More formal and professional
        evolved_traits["formality"] *= 1.2
        evolved_traits["patience"] *= 1.1
    
    return {**base_personality, "traits": evolved_traits}
```

### Context-Based Personality Selection

```python
# Select personality based on user context
async def select_personality_for_context(user_id: str, context: str):
    user_facts = await client.get_facts(user_id)
    
    # Check user preferences
    language_pref = next((f["value"] for f in user_facts if f["key"] == "language"), "en")
    tech_level = next((f["value"] for f in user_facts if f["key"] == "tech_savvy"), "intermediate")
    
    if context == "technical_support" and tech_level == "beginner":
        return "patient_technical_assistant"
    elif context == "billing" and language_pref == "es":
        return "billing_assistant_es"
    else:
        return "default_assistant"
```

## Testing Personalities

### Unit Testing

```python
import pytest
from luminoracore import Personality

def test_personality_creation():
    personality_data = load_test_personality()
    personality = Personality(personality_data)
    
    assert personality.name == "test_assistant"
    assert personality.traits["helpfulness"] == 0.9
    assert len(personality.examples) > 0

def test_personality_validation():
    validator = PersonalityValidator()
    personality_data = load_test_personality()
    
    is_valid = validator.validate_personality(personality_data)
    assert is_valid == True
```

### Integration Testing

```python
async def test_personality_interaction():
    client = LuminoraCoreClientV11(...)
    
    # Create session with personality
    session_id = await client.create_session(
        personality_name="test_assistant",
        provider_config={"name": "openai", "model": "gpt-3.5-turbo"}
    )
    
    # Test interaction
    response = await client.send_message_with_memory(
        session_id=session_id,
        user_message="Hello, I need help",
        personality_name="test_assistant",
        provider_config={"name": "openai", "model": "gpt-3.5-turbo"}
    )
    
    assert response["success"] == True
    assert len(response["response"]) > 0
```

### A/B Testing

```python
# Test different personality variations
async def ab_test_personalities(user_id: str, message: str):
    personalities = ["formal_assistant", "casual_assistant"]
    
    results = {}
    for personality_name in personalities:
        response = await client.send_message_with_memory(
            session_id=user_id,
            user_message=message,
            personality_name=personality_name,
            provider_config={"name": "openai", "model": "gpt-3.5-turbo"}
        )
        results[personality_name] = response
    
    return results
```

## Deployment Strategies

### Gradual Rollout

```python
# Deploy personality to subset of users
async def deploy_personality(personality_name: str, rollout_percentage: float):
    eligible_users = get_users_for_rollout(rollout_percentage)
    
    for user_id in eligible_users:
        await set_user_personality(user_id, personality_name)
    
    # Monitor performance
    await monitor_personality_performance(personality_name)
```

### Feature Flags

```python
# Use feature flags for personality variants
class PersonalityFeatureFlags:
    def __init__(self):
        self.flags = {
            "new_support_personality": False,
            "enhanced_empathy": True,
            "technical_expert_mode": False
        }
    
    def get_personality_config(self, base_personality: dict) -> dict:
        config = base_personality.copy()
        
        if self.flags["enhanced_empathy"]:
            config["traits"]["empathy"] *= 1.2
        
        if self.flags["technical_expert_mode"]:
            config["traits"]["technical_knowledge"] = 0.9
        
        return config
```

## Best Practices

### 1. Personality Design

- **Start Simple**: Begin with basic traits and add complexity
- **Be Consistent**: Ensure traits, rules, and examples align
- **Test Thoroughly**: Validate with real user interactions
- **Document Changes**: Keep track of personality modifications

### 2. System Prompt Writing

- **Be Specific**: Clearly define the personality's role and capabilities
- **Include Guidelines**: Provide specific behavior instructions
- **Set Boundaries**: Define what the personality should and shouldn't do
- **Use Examples**: Include sample interactions in the prompt

### 3. Example Quality

- **Be Realistic**: Use examples that reflect real user interactions
- **Show Diversity**: Include various scenarios and user types
- **Match Personality**: Ensure examples reflect the defined traits
- **Include Edge Cases**: Cover challenging situations

### 4. Testing Strategy

- **Unit Tests**: Test individual personality components
- **Integration Tests**: Test personality interactions with the system
- **User Testing**: Validate with real users
- **Performance Testing**: Ensure personality responses are fast

## Monitoring and Analytics

### Personality Performance Metrics

```python
class PersonalityAnalytics:
    def track_interaction(self, personality: str, user_id: str, satisfaction: float):
        self.metrics.gauge("personality.satisfaction", satisfaction, tags={
            "personality": personality,
            "user_id": user_id
        })
    
    def track_response_time(self, personality: str, duration: float):
        self.metrics.histogram("personality.response_time", duration, tags={
            "personality": personality
        })
```

### User Feedback Collection

```python
async def collect_user_feedback(session_id: str, personality_name: str):
    feedback = await request_user_feedback(session_id)
    
    if feedback:
        await save_feedback({
            "session_id": session_id,
            "personality": personality_name,
            "rating": feedback["rating"],
            "comments": feedback["comments"],
            "timestamp": datetime.now()
        })
```

## Conclusion

Creating effective AI personalities with LuminoraCore v1.1 requires careful design, thorough testing, and continuous monitoring. By following these guidelines and best practices, you can build personalities that provide meaningful, engaging experiences for your users.

### Key Success Factors

1. **Clear Personality Definition**: Well-defined traits, rules, and examples
2. **Quality Training Data**: Realistic, diverse examples
3. **Thorough Testing**: Unit, integration, and user testing
4. **Continuous Monitoring**: Track performance and user satisfaction
5. **Iterative Improvement**: Regular updates based on feedback

**Start building your AI personalities today with LuminoraCore v1.1.**