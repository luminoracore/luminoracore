"""Streamlit integration example for LuminoraCore SDK."""

import streamlit as st
import asyncio
import os
from typing import Optional

from luminoracore import LuminoraCoreClient
from luminoracore.types.provider import ProviderConfig
from luminoracore.types.session import StorageConfig, MemoryConfig


# Initialize Streamlit page
st.set_page_config(
    page_title="LuminoraCore Demo",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 LuminoraCore Demo")
st.markdown("Advanced AI Personality Management with LuminoraCore SDK")


@st.cache_resource
def get_client():
    """Get or create the LuminoraCore client."""
    client = LuminoraCoreClient(
        storage_config=StorageConfig(
            storage_type="memory",
            ttl=3600
        ),
        memory_config=MemoryConfig(
            max_tokens=10000,
            max_messages=100,
            ttl=1800
        )
    )
    return client


async def initialize_client():
    """Initialize the client."""
    client = get_client()
    if not hasattr(client, '_initialized'):
        await client.initialize()
        client._initialized = True
    return client


def main():
    """Main Streamlit app."""
    # Initialize client
    client = asyncio.run(initialize_client())
    
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    
    # Provider configuration
    st.sidebar.subheader("Provider Settings")
    provider_name = st.sidebar.selectbox(
        "Provider",
        ["openai", "anthropic", "mistral", "cohere", "google"]
    )
    
    model = st.sidebar.selectbox(
        "Model",
        ["gpt-3.5-turbo", "gpt-4", "claude-3-sonnet", "mistral-tiny", "command", "gemini-pro"]
    )
    
    api_key = st.sidebar.text_input(
        "API Key",
        type="password",
        value=os.getenv(f"{provider_name.upper()}_API_KEY", "")
    )
    
    # Personality configuration
    st.sidebar.subheader("Personality Settings")
    personality_name = st.sidebar.selectbox(
        "Personality",
        ["helpful_assistant", "creative_writer", "technical_expert", "friendly_chatbot"]
    )
    
    # Session management
    st.sidebar.subheader("Session Management")
    
    if st.sidebar.button("Create New Session"):
        if not api_key:
            st.error("Please enter an API key")
        else:
            try:
                provider_config = ProviderConfig(
                    name=provider_name,
                    api_key=api_key,
                    model=model,
                    timeout=30,
                    max_retries=3
                )
                
                session_id = asyncio.run(client.create_session(
                    personality_name=personality_name,
                    provider_config=provider_config
                ))
                
                st.session_state.session_id = session_id
                st.success(f"Created session: {session_id}")
            except Exception as e:
                st.error(f"Failed to create session: {e}")
    
    if st.sidebar.button("Clear Session"):
        if "session_id" in st.session_state:
            asyncio.run(client.clear_conversation(st.session_state.session_id))
            st.success("Session cleared")
    
    # Main chat interface
    if "session_id" not in st.session_state:
        st.info("Please create a session to start chatting")
        return
    
    st.header("Chat Interface")
    
    # Display conversation history
    messages = asyncio.run(client.get_conversation(st.session_state.session_id))
    
    if messages:
        st.subheader("Conversation History")
        for message in messages:
            if message.role == "user":
                st.write(f"**You:** {message.content}")
            else:
                st.write(f"**Assistant:** {message.content}")
    
    # Message input
    user_message = st.text_input("Enter your message:", key="user_input")
    
    if st.button("Send Message"):
        if user_message:
            try:
                response = asyncio.run(client.send_message(
                    session_id=st.session_state.session_id,
                    message=user_message
                ))
                
                st.success("Message sent successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to send message: {e}")
    
    # Session info
    st.subheader("Session Information")
    info = asyncio.run(client.get_session_info(st.session_state.session_id))
    if info:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Session ID", info["session_id"][:8] + "...")
        with col2:
            st.metric("Personality", info["personality"])
        with col3:
            st.metric("Message Count", info["message_count"])
    
    # Personality blending demo
    st.header("Personality Blending Demo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Available Personalities")
        personalities = asyncio.run(client.list_personalities())
        if personalities:
            st.write("Available personalities:")
            for personality in personalities:
                st.write(f"- {personality}")
        else:
            st.write("No personalities loaded")
    
    with col2:
        st.subheader("Blend Personalities")
        
        # Personality selection for blending
        personality1 = st.selectbox("First Personality", personalities)
        personality2 = st.selectbox("Second Personality", personalities)
        
        # Weight selection
        weight1 = st.slider("Weight for first personality", 0.0, 1.0, 0.5)
        weight2 = 1.0 - weight1
        
        st.write(f"Weights: {personality1} ({weight1:.1f}), {personality2} ({weight2:.1f})")
        
        if st.button("Create Blended Personality"):
            try:
                blended = asyncio.run(client.blend_personalities(
                    personality_names=[personality1, personality2],
                    weights=[weight1, weight2],
                    blend_name=f"{personality1}_{personality2}_blend"
                ))
                
                if blended:
                    st.success(f"Created blended personality: {blended.name}")
                    st.write(f"Description: {blended.description}")
                else:
                    st.error("Failed to create blended personality")
            except Exception as e:
                st.error(f"Error creating blended personality: {e}")


if __name__ == "__main__":
    main()
