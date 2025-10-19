#!/usr/bin/env python3
"""
Performance Comparison: Old vs New Conversation Memory Approach

This test measures the performance impact of the conversation memory fix
to ensure it doesn't make conversations slower for users.
"""

import asyncio
import time
import json
from datetime import datetime
from typing import Dict, List, Any
import statistics


class PerformanceTest:
    """Test performance impact of conversation memory fix"""
    
    def __init__(self):
        self.results = {
            "old_approach": [],
            "new_approach": [],
            "context_sizes": [],
            "token_estimates": []
        }
    
    async def test_old_approach(self, messages: List[str], iterations: int = 10):
        """Test old approach (individual messages without context)"""
        
        print("Testing OLD APPROACH (Individual messages)...")
        
        for i in range(iterations):
            start_time = time.time()
            
            # Simulate old approach - just send current message
            for message in messages:
                # Mock LLM call with just current message
                context = f"Current message: {message}"
                response = self._mock_llm_call(context)
                
                # No memory operations
                # No context building
                # No fact extraction
            
            end_time = time.time()
            total_time = end_time - start_time
            
            self.results["old_approach"].append(total_time)
            print(f"  Iteration {i+1}: {total_time:.4f}s")
        
        avg_time = statistics.mean(self.results["old_approach"])
        print(f"  Average time: {avg_time:.4f}s")
        print()
    
    async def test_new_approach(self, messages: List[str], iterations: int = 10):
        """Test new approach (with full conversation context)"""
        
        print("Testing NEW APPROACH (With conversation memory)...")
        
        for i in range(iterations):
            start_time = time.time()
            
            # Simulate new approach - build full context
            conversation_history = []
            user_facts = []
            affinity = {"level": "stranger", "points": 0}
            
            for j, message in enumerate(messages):
                # Build full context
                context = self._build_full_context(
                    conversation_history, user_facts, affinity, message
                )
                
                # Mock LLM call with full context
                response = self._mock_llm_call(context)
                
                # Extract and save facts
                new_facts = self._extract_facts(message)
                user_facts.extend(new_facts)
                
                # Update conversation history
                conversation_history.append({
                    "user_message": message,
                    "assistant_response": response,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Update affinity
                affinity["points"] += 1
                if affinity["points"] >= 25:
                    affinity["level"] = "acquaintance"
                elif affinity["points"] >= 50:
                    affinity["level"] = "friend"
                
                # Track context size
                context_size = len(context)
                self.results["context_sizes"].append(context_size)
                
                # Estimate tokens (rough: 1 token ≈ 4 characters)
                token_estimate = context_size // 4
                self.results["token_estimates"].append(token_estimate)
            
            end_time = time.time()
            total_time = end_time - start_time
            
            self.results["new_approach"].append(total_time)
            print(f"  Iteration {i+1}: {total_time:.4f}s")
        
        avg_time = statistics.mean(self.results["new_approach"])
        print(f"  Average time: {avg_time:.4f}s")
        print()
    
    def _build_full_context(
        self, 
        conversation_history: List[Dict], 
        user_facts: List[Dict], 
        affinity: Dict, 
        current_message: str
    ) -> str:
        """Build full context for LLM"""
        
        context_parts = []
        
        # Personality and relationship
        context_parts.append(f"Personality: sakura")
        context_parts.append(f"Relationship Level: {affinity['level']} ({affinity['points']}/100 points)")
        
        # User facts
        if user_facts:
            facts_context = "User Facts: "
            facts_list = [f"{fact['key']}: {fact['value']}" for fact in user_facts]
            facts_context += ", ".join(facts_list)
            context_parts.append(facts_context)
        
        # Conversation history
        if conversation_history:
            history_context = "Conversation History:\n"
            for turn in conversation_history[-5:]:  # Last 5 turns
                history_context += f"User: {turn['user_message']}\n"
                history_context += f"Assistant: {turn['assistant_response']}\n"
            context_parts.append(history_context)
        
        # Instructions based on relationship
        if affinity['level'] == 'stranger':
            context_parts.append("Instructions: Be professional and formal.")
        elif affinity['level'] == 'acquaintance':
            context_parts.append("Instructions: Be friendly and polite.")
        elif affinity['level'] == 'friend':
            context_parts.append("Instructions: Be casual and friendly.")
        
        # Current message
        context_parts.append(f"Current User Message: {current_message}")
        
        return "\n\n".join(context_parts)
    
    def _mock_llm_call(self, context: str) -> str:
        """Mock LLM call - simulate processing time"""
        
        # Simulate LLM processing time based on context size
        # Real LLM calls take time proportional to context length
        processing_time = len(context) * 0.00001  # 0.01ms per character
        time.sleep(processing_time)
        
        return f"Response to: {context[:50]}..."
    
    def _extract_facts(self, message: str) -> List[Dict]:
        """Extract facts from message"""
        
        facts = []
        message_lower = message.lower()
        
        # Simple fact extraction
        if "soy" in message_lower or "me llamo" in message_lower:
            words = message.split()
            for i, word in enumerate(words):
                if word.lower() in ["soy", "me", "llamo"]:
                    if i + 1 < len(words):
                        name = words[i + 1].strip(".,!?")
                        if len(name) > 1 and name.isalpha():
                            facts.append({
                                "key": "name",
                                "value": name,
                                "confidence": 0.9
                            })
                            break
        
        return facts
    
    def analyze_results(self):
        """Analyze performance results"""
        
        print("PERFORMANCE ANALYSIS")
        print("=" * 50)
        
        # Time comparison
        old_avg = statistics.mean(self.results["old_approach"])
        new_avg = statistics.mean(self.results["new_approach"])
        
        print(f"OLD APPROACH (Individual messages):")
        print(f"  Average time: {old_avg:.4f}s")
        print(f"  Min time: {min(self.results['old_approach']):.4f}s")
        print(f"  Max time: {max(self.results['old_approach']):.4f}s")
        
        print(f"\nNEW APPROACH (With conversation memory):")
        print(f"  Average time: {new_avg:.4f}s")
        print(f"  Min time: {min(self.results['new_approach']):.4f}s")
        print(f"  Max time: {max(self.results['new_approach']):.4f}s")
        
        # Performance impact
        time_increase = new_avg - old_avg
        time_increase_percent = (time_increase / old_avg) * 100
        
        print(f"\nPERFORMANCE IMPACT:")
        print(f"  Time increase: {time_increase:.4f}s ({time_increase_percent:.1f}%)")
        
        if time_increase_percent < 10:
            print(f"  IMPACT: MINIMAL - Less than 10% increase")
        elif time_increase_percent < 25:
            print(f"  IMPACT: MODERATE - 10-25% increase")
        else:
            print(f"  IMPACT: SIGNIFICANT - More than 25% increase")
        
        # Context size analysis
        if self.results["context_sizes"]:
            avg_context_size = statistics.mean(self.results["context_sizes"])
            max_context_size = max(self.results["context_sizes"])
            
            print(f"\nCONTEXT SIZE ANALYSIS:")
            print(f"  Average context size: {avg_context_size:.0f} characters")
            print(f"  Maximum context size: {max_context_size:.0f} characters")
            
            # Token estimates
            if self.results["token_estimates"]:
                avg_tokens = statistics.mean(self.results["token_estimates"])
                max_tokens = max(self.results["token_estimates"])
                
                print(f"  Average tokens: {avg_tokens:.0f}")
                print(f"  Maximum tokens: {max_tokens:.0f}")
                
                # Cost impact (rough estimate)
                # Assuming $0.002 per 1K tokens for GPT-4
                cost_per_1k_tokens = 0.002
                additional_cost_per_message = (avg_tokens - 50) * cost_per_1k_tokens / 1000
                
                print(f"  Additional cost per message: ~${additional_cost_per_message:.4f}")
        
        # User experience impact
        print(f"\nUSER EXPERIENCE IMPACT:")
        if time_increase < 0.1:  # Less than 100ms
            print(f"  IMPACT: NEGLIGIBLE - Users won't notice the difference")
        elif time_increase < 0.5:  # Less than 500ms
            print(f"  IMPACT: MINIMAL - Slight delay, but acceptable")
        elif time_increase < 1.0:  # Less than 1 second
            print(f"  IMPACT: MODERATE - Noticeable delay, but manageable")
        else:
            print(f"  IMPACT: SIGNIFICANT - Users will notice slower responses")
        
        return {
            "time_increase": time_increase,
            "time_increase_percent": time_increase_percent,
            "avg_context_size": avg_context_size if self.results["context_sizes"] else 0,
            "avg_tokens": avg_tokens if self.results["token_estimates"] else 0
        }


async def main():
    """Main performance test"""
    
    print("PERFORMANCE COMPARISON: Old vs New Conversation Memory")
    print("=" * 60)
    print("Testing if the conversation memory fix makes conversations slower")
    print()
    
    # Test messages (simulating a conversation)
    test_messages = [
        "ire al himalaya que te parece, soy carlos",
        "como te llamas?",
        "vaya no lo sabes??",
        "que opinas del viaje?",
        "tienes algun consejo?"
    ]
    
    print(f"Test scenario: {len(test_messages)} messages in conversation")
    print()
    
    # Initialize performance test
    perf_test = PerformanceTest()
    
    # Test old approach
    await perf_test.test_old_approach(test_messages, iterations=5)
    
    # Test new approach
    await perf_test.test_new_approach(test_messages, iterations=5)
    
    # Analyze results
    results = perf_test.analyze_results()
    
    print("\n" + "=" * 60)
    print("CONCLUSION")
    print("=" * 60)
    
    if results["time_increase_percent"] < 25:
        print("✅ ACCEPTABLE: The conversation memory fix has minimal performance impact.")
        print("   Users will not experience significantly slower conversations.")
        print("   The benefits of memory far outweigh the small performance cost.")
    else:
        print("⚠️  CONCERNING: The conversation memory fix has significant performance impact.")
        print("   Users may notice slower conversations.")
        print("   Consider optimization strategies.")
    
    print(f"\nKey metrics:")
    print(f"  - Time increase: {results['time_increase_percent']:.1f}%")
    print(f"  - Average context size: {results['avg_context_size']:.0f} characters")
    print(f"  - Average tokens: {results['avg_tokens']:.0f}")
    
    print(f"\nRecommendation:")
    if results["time_increase_percent"] < 10:
        print("  ✅ Deploy the fix - performance impact is negligible")
    elif results["time_increase_percent"] < 25:
        print("  ✅ Deploy the fix - performance impact is acceptable")
    else:
        print("  ⚠️  Optimize before deploying - performance impact is significant")


if __name__ == "__main__":
    asyncio.run(main())
