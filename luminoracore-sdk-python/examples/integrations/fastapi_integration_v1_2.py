"""
FastAPI integration example for LuminoraCore SDK v1.2.0 with Optimization.

This example demonstrates:
- FastAPI REST API
- Optimization features (NEW in v1.2.0)
- Token reduction (25-45%)
- Transparent compression/expansion
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import asyncio
import os

from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.types.provider import ProviderConfig
from luminoracore_sdk.types.session import StorageConfig, MemoryConfig

# Import optimization from Core
try:
    from luminoracore.optimization import OptimizationConfig
    HAS_OPTIMIZATION = True
except ImportError:
    HAS_OPTIMIZATION = False
    OptimizationConfig = None


# Pydantic models
class SessionCreate(BaseModel):
    personality_name: str
    provider_name: str
    model: str
    api_key: str


class MessageSend(BaseModel):
    message: str
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None


class MessageResponse(BaseModel):
    content: str
    role: str
    finish_reason: Optional[str]
    usage: Optional[dict]
    model: Optional[str]


class SessionInfo(BaseModel):
    session_id: str
    personality: str
    provider: str
    model: str
    created_at: str
    last_activity: str
    message_count: int


class OptimizationStats(BaseModel):
    enabled: bool
    config: dict
    stats: Optional[dict] = None


# Initialize FastAPI app
app = FastAPI(title="LuminoraCore API v1.2.0", version="1.2.0")

# Initialize LuminoraCore client with optimization
if HAS_OPTIMIZATION:
    opt_config = OptimizationConfig(
        key_abbreviation=True,
        compact_format=True,
        minification=True,
        deduplication=True,
        cache_enabled=True,
        cache_size=1000,
        cache_ttl=3600
    )
else:
    opt_config = None

client = LuminoraCoreClient(
    storage_config=StorageConfig(
        storage_type="memory",
        ttl=3600
    ),
    memory_config=MemoryConfig(
        max_tokens=10000,
        max_messages=100,
        ttl=1800
    ),
    optimization_config=opt_config  # 🆕 NEW in v1.2.0
)


@app.on_event("startup")
async def startup_event():
    """Initialize the LuminoraCore client on startup."""
    await client.initialize()
    if HAS_OPTIMIZATION:
        print("[INFO] Optimization enabled - Token reduction: 25-45%")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up the LuminoraCore client on shutdown."""
    await client.cleanup()


@app.post("/sessions", response_model=dict)
async def create_session(session_data: SessionCreate):
    """Create a new session."""
    try:
        provider_config = ProviderConfig(
            name=session_data.provider_name,
            api_key=session_data.api_key,
            model=session_data.model,
            timeout=30,
            max_retries=3
        )
        
        session_id = await client.create_session(
            personality_name=session_data.personality_name,
            provider_config=provider_config
        )
        
        return {"session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/sessions/{session_id}/messages", response_model=MessageResponse)
async def send_message(session_id: str, message_data: MessageSend):
    """Send a message to a session."""
    try:
        response = await client.send_message(
            session_id=session_id,
            message=message_data.message,
            temperature=message_data.temperature,
            max_tokens=message_data.max_tokens
        )
        
        return MessageResponse(
            content=response.content,
            role=response.role,
            finish_reason=response.finish_reason,
            usage=response.usage,
            model=response.model
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/sessions/{session_id}/messages", response_model=List[dict])
async def get_conversation(session_id: str):
    """Get conversation history for a session."""
    try:
        messages = await client.get_conversation(session_id)
        if messages is None:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in messages
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/sessions/{session_id}/messages")
async def clear_conversation(session_id: str):
    """Clear conversation history for a session."""
    try:
        result = await client.clear_conversation(session_id)
        if not result:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return {"message": "Conversation cleared"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a session."""
    try:
        result = await client.delete_session(session_id)
        if not result:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return {"message": "Session deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/sessions", response_model=List[str])
async def list_sessions():
    """List all active sessions."""
    try:
        sessions = await client.list_sessions()
        return sessions
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/sessions/{session_id}/info", response_model=SessionInfo)
async def get_session_info(session_id: str):
    """Get session information."""
    try:
        info = await client.get_session_info(session_id)
        if info is None:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return SessionInfo(**info)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/personalities", response_model=List[str])
async def list_personalities():
    """List all available personalities."""
    try:
        personalities = await client.list_personalities()
        return personalities
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/personalities/blend", response_model=dict)
async def blend_personalities(
    personality_names: List[str],
    weights: List[float],
    blend_name: Optional[str] = None
):
    """Blend multiple personalities."""
    try:
        blended = await client.blend_personalities(
            personality_names=personality_names,
            weights=weights,
            blend_name=blend_name
        )
        
        if blended is None:
            raise HTTPException(status_code=400, detail="Failed to blend personalities")
        
        return {
            "name": blended.name,
            "description": blended.description,
            "metadata": blended.metadata
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/optimization/stats", response_model=OptimizationStats)
async def get_optimization_stats():
    """Get optimization statistics (NEW in v1.2.0)."""
    try:
        if not HAS_OPTIMIZATION:
            return OptimizationStats(
                enabled=False,
                config={},
                stats={"message": "Optimization not available. Install luminoracore>=1.2.0"}
            )
        
        stats = await client.get_optimization_stats()
        return OptimizationStats(**stats)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "LuminoraCore API",
        "version": "1.2.0",
        "optimization": HAS_OPTIMIZATION
    }


if __name__ == "__main__":
    import uvicorn
    print("[INFO] Starting LuminoraCore API v1.2.0 with Optimization")
    print(f"[INFO] Optimization available: {HAS_OPTIMIZATION}")
    uvicorn.run(app, host="0.0.0.0", port=8000)

