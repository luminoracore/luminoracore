"""Command-line interface for LuminoraCore SDK."""

import asyncio
import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from .client import LuminoraCoreClient
from .types.provider import ProviderConfig
from .types.session import StorageConfig, MemoryConfig
from .utils.exceptions import LuminoraCoreSDKError


async def create_session_command(args):
    """Create a new session."""
    client = LuminoraCoreClient()
    await client.initialize()
    
    try:
        provider_config = ProviderConfig(
            name=args.provider,
            api_key=args.api_key,
            model=args.model,
            base_url=args.base_url,
            timeout=args.timeout,
            max_retries=args.max_retries
        )
        
        session_id = await client.create_session(
            personality_name=args.personality,
            provider_config=provider_config
        )
        
        print(f"Created session: {session_id}")
        
    except Exception as e:
        print(f"Error creating session: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        await client.cleanup()


async def send_message_command(args):
    """Send a message to a session."""
    client = LuminoraCoreClient()
    await client.initialize()
    
    try:
        response = await client.send_message(
            session_id=args.session_id,
            message=args.message,
            temperature=args.temperature,
            max_tokens=args.max_tokens
        )
        
        print(response.content)
        
    except Exception as e:
        print(f"Error sending message: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        await client.cleanup()


async def list_sessions_command(args):
    """List all sessions."""
    client = LuminoraCoreClient()
    await client.initialize()
    
    try:
        sessions = await client.list_sessions()
        
        if not sessions:
            print("No active sessions")
            return
        
        for session_id in sessions:
            info = await client.get_session_info(session_id)
            if info:
                print(f"Session: {session_id}")
                print(f"  Personality: {info['personality']}")
                print(f"  Provider: {info['provider']}")
                print(f"  Model: {info['model']}")
                print(f"  Messages: {info['message_count']}")
                print()
        
    except Exception as e:
        print(f"Error listing sessions: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        await client.cleanup()


async def list_personalities_command(args):
    """List all personalities."""
    client = LuminoraCoreClient()
    await client.initialize()
    
    try:
        personalities = await client.list_personalities()
        
        if not personalities:
            print("No personalities loaded")
            return
        
        for personality_name in personalities:
            personality = await client.get_personality(personality_name)
            if personality:
                print(f"Personality: {personality.name}")
                print(f"  Description: {personality.description}")
                print(f"  System Prompt Length: {len(personality.system_prompt)}")
                print()
        
    except Exception as e:
        print(f"Error listing personalities: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        await client.cleanup()


async def blend_personalities_command(args):
    """Blend personalities."""
    client = LuminoraCoreClient()
    await client.initialize()
    
    try:
        # Parse weights
        weights = [float(w) for w in args.weights]
        
        # Validate weights sum to 1.0
        if abs(sum(weights) - 1.0) > 0.01:
            print("Error: Weights must sum to 1.0", file=sys.stderr)
            sys.exit(1)
        
        blended = await client.blend_personalities(
            personality_names=args.personalities,
            weights=weights,
            blend_name=args.name
        )
        
        if blended:
            print(f"Created blended personality: {blended.name}")
            print(f"Description: {blended.description}")
        else:
            print("Failed to create blended personality", file=sys.stderr)
            sys.exit(1)
        
    except Exception as e:
        print(f"Error blending personalities: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        await client.cleanup()


async def load_personality_command(args):
    """Load a personality from a file."""
    client = LuminoraCoreClient()
    await client.initialize()
    
    try:
        # Load personality from file
        with open(args.file, 'r') as f:
            config = json.load(f)
        
        name = config.get("name", Path(args.file).stem)
        
        success = await client.load_personality(name, config)
        
        if success:
            print(f"Loaded personality: {name}")
        else:
            print("Failed to load personality", file=sys.stderr)
            sys.exit(1)
        
    except Exception as e:
        print(f"Error loading personality: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        await client.cleanup()


async def get_client_info_command(args):
    """Get client information."""
    client = LuminoraCoreClient()
    await client.initialize()
    
    try:
        info = await client.get_client_info()
        
        print(json.dumps(info, indent=2))
        
    except Exception as e:
        print(f"Error getting client info: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        await client.cleanup()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="LuminoraCore SDK CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create session command
    create_parser = subparsers.add_parser("create-session", help="Create a new session")
    create_parser.add_argument("--personality", required=True, help="Personality name")
    create_parser.add_argument("--provider", required=True, help="Provider name")
    create_parser.add_argument("--api-key", required=True, help="API key")
    create_parser.add_argument("--model", required=True, help="Model name")
    create_parser.add_argument("--base-url", help="Base URL")
    create_parser.add_argument("--timeout", type=int, default=30, help="Timeout in seconds")
    create_parser.add_argument("--max-retries", type=int, default=3, help="Max retries")
    
    # Send message command
    send_parser = subparsers.add_parser("send-message", help="Send a message to a session")
    send_parser.add_argument("--session-id", required=True, help="Session ID")
    send_parser.add_argument("--message", required=True, help="Message to send")
    send_parser.add_argument("--temperature", type=float, default=0.7, help="Temperature")
    send_parser.add_argument("--max-tokens", type=int, help="Max tokens")
    
    # List sessions command
    subparsers.add_parser("list-sessions", help="List all sessions")
    
    # List personalities command
    subparsers.add_parser("list-personalities", help="List all personalities")
    
    # Blend personalities command
    blend_parser = subparsers.add_parser("blend-personalities", help="Blend personalities")
    blend_parser.add_argument("--personalities", nargs="+", required=True, help="Personality names")
    blend_parser.add_argument("--weights", nargs="+", required=True, help="Weights")
    blend_parser.add_argument("--name", help="Blend name")
    
    # Load personality command
    load_parser = subparsers.add_parser("load-personality", help="Load a personality from file")
    load_parser.add_argument("--file", required=True, help="Personality file path")
    
    # Get client info command
    subparsers.add_parser("info", help="Get client information")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Map commands to functions
    command_map = {
        "create-session": create_session_command,
        "send-message": send_message_command,
        "list-sessions": list_sessions_command,
        "list-personalities": list_personalities_command,
        "blend-personalities": blend_personalities_command,
        "load-personality": load_personality_command,
        "info": get_client_info_command,
    }
    
    # Execute command
    command_func = command_map[args.command]
    asyncio.run(command_func(args))


if __name__ == "__main__":
    main()
