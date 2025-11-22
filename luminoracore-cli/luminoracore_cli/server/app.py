"""FastAPI application for LuminoraCore development server."""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import json
import asyncio

from pathlib import Path

from luminoracore_cli.utils.errors import CLIError
from luminoracore_cli.core.client import get_client


def create_app(api_only: bool = False, cors: bool = False) -> FastAPI:
    """
    Create FastAPI application.
    
    Args:
        api_only: If True, only API endpoints (no web UI)
        cors: Enable CORS middleware
    
    Returns:
        FastAPI application instance
    """
    app = FastAPI(
        title="LuminoraCore Development Server",
        description="Local development server for LuminoraCore personalities",
        version="1.0.0"
    )
    
    # Add CORS middleware if enabled
    if cors:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    # Mount static files if not API only
    if not api_only:
        try:
            static_dir = Path(__file__).parent / "static"
            if static_dir.exists():
                app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
        except Exception:
            pass  # Static files not available
    
    # API endpoints
    @app.get("/")
    async def root():
        """Root endpoint."""
        if api_only:
            return {"message": "LuminoraCore Development Server API", "version": "1.0.0"}
        else:
            return HTMLResponse(get_web_ui_html())
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        try:
            client = get_client()
            health = await client.health_check()
            return health
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
    
    @app.get("/api/personalities")
    async def list_personalities():
        """List available personalities."""
        try:
            client = get_client()
            personalities = await client.list_personalities()
            return {"personalities": personalities}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/personalities/{personality_id}")
    async def get_personality(personality_id: str):
        """Get personality details."""
        try:
            client = get_client()
            personality = await client.get_personality(personality_id)
            return personality
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
    
    @app.post("/api/compile")
    async def compile_personality(request: CompileRequest):
        """Compile personality to prompt."""
        try:
            client = get_client()
            result = await client.compile_personality(
                personality_data=request.personality_data,
                provider=request.provider,
                model=request.model,
                include_metadata=request.include_metadata
            )
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/validate")
    async def validate_personality(request: ValidateRequest):
        """Validate personality data."""
        try:
            client = get_client()
            result = await client.validate_personality(
                personality_data=request.personality_data,
                strict=request.strict
            )
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/blend")
    async def blend_personalities(request: BlendRequest):
        """Blend multiple personalities."""
        try:
            client = get_client()
            result = await client.blend_personalities(
                personality_weights=request.personality_weights,
                custom_name=request.custom_name
            )
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/test")
    async def test_personality(request: TestRequest):
        """Test personality with LLM provider."""
        try:
            client = get_client()
            result = await client.test_personality(
                personality_data=request.personality_data,
                provider=request.provider,
                model=request.model,
                test_message=request.test_message
            )
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # WebSocket chat endpoint
    @app.websocket("/ws/chat")
    async def websocket_chat(websocket: WebSocket):
        """WebSocket chat endpoint."""
        await websocket.accept()
        
        try:
            while True:
                # Receive message
                data = await websocket.receive_json()
                
                # Process message
                if data.get("type") == "chat":
                    # Handle chat message
                    response = await handle_chat_message(data)
                    await websocket.send_json(response)
                elif data.get("type") == "ping":
                    # Handle ping
                    await websocket.send_json({"type": "pong"})
                else:
                    # Unknown message type
                    await websocket.send_json({"type": "error", "message": "Unknown message type"})
        
        except WebSocketDisconnect:
            pass
        except Exception as e:
            await websocket.send_json({"type": "error", "message": str(e)})
    
    return app


async def handle_chat_message(data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle chat message from WebSocket."""
    try:
        personality_id = data.get("personality_id")
        message = data.get("message", "")
        provider = data.get("provider", "openai")
        model = data.get("model")
        
        if not personality_id:
            return {"type": "error", "message": "Personality ID required"}
        
        if not message:
            return {"type": "error", "message": "Message required"}
        
        # Get personality
        client = get_client()
        personality = await client.get_personality(personality_id)
        
        # Test personality
        result = await client.test_personality(
            personality_data=personality,
            provider=provider,
            model=model,
            test_message=message
        )
        
        # Extract response
        response = result.get("test_result", {}).get("response", "No response")
        
        return {
            "type": "chat_response",
            "response": response,
            "personality_id": personality_id,
            "provider": provider,
            "model": model
        }
        
    except Exception as e:
        return {"type": "error", "message": str(e)}


def get_web_ui_html() -> str:
    """Get web UI HTML."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LuminoraCore Development Server</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background: white;
                border-radius: 8px;
                padding: 30px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                text-align: center;
                margin-bottom: 30px;
            }
            .section {
                margin-bottom: 30px;
                padding: 20px;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
            }
            .section h2 {
                margin-top: 0;
                color: #555;
            }
            .endpoint {
                background: #f8f9fa;
                padding: 10px;
                margin: 10px 0;
                border-radius: 4px;
                font-family: monospace;
            }
            .method {
                display: inline-block;
                padding: 2px 8px;
                border-radius: 3px;
                font-size: 12px;
                font-weight: bold;
                margin-right: 10px;
            }
            .get { background: #28a745; color: white; }
            .post { background: #007bff; color: white; }
            .ws { background: #6f42c1; color: white; }
            .chat-container {
                max-width: 600px;
                margin: 20px auto;
                border: 1px solid #ddd;
                border-radius: 8px;
                overflow: hidden;
            }
            .chat-messages {
                height: 400px;
                overflow-y: auto;
                padding: 20px;
                background: #f9f9f9;
            }
            .message {
                margin-bottom: 15px;
                padding: 10px;
                border-radius: 6px;
            }
            .user-message {
                background: #007bff;
                color: white;
                margin-left: 20%;
            }
            .bot-message {
                background: white;
                border: 1px solid #ddd;
                margin-right: 20%;
            }
            .chat-input {
                display: flex;
                padding: 15px;
                background: white;
                border-top: 1px solid #ddd;
            }
            .chat-input input {
                flex: 1;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-right: 10px;
            }
            .chat-input button {
                padding: 10px 20px;
                background: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            .chat-input button:hover {
                background: #0056b3;
            }
            .status {
                padding: 10px;
                background: #e9ecef;
                border-radius: 4px;
                margin-bottom: 20px;
            }
            .connected { background: #d4edda; color: #155724; }
            .disconnected { background: #f8d7da; color: #721c24; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 LuminoraCore Development Server</h1>
            
            <div class="status" id="status">
                <strong>Status:</strong> <span id="status-text">Connecting...</span>
            </div>
            
            <div class="section">
                <h2>📋 Available Endpoints</h2>
                <div class="endpoint">
                    <span class="method get">GET</span> / - This web interface
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> /health - Health check
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> /api/personalities - List personalities
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> /api/personalities/{id} - Get personality
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> /api/compile - Compile personality
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> /api/validate - Validate personality
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> /api/blend - Blend personalities
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> /api/test - Test personality
                </div>
                <div class="endpoint">
                    <span class="method ws">WS</span> /ws/chat - WebSocket chat
                </div>
            </div>
            
            <div class="section">
                <h2>💬 Interactive Chat</h2>
                <div class="chat-container">
                    <div class="chat-messages" id="chat-messages">
                        <div class="message bot-message">
                            <strong>LuminoraCore:</strong> Hello! I'm ready to chat. Select a personality and start typing!
                        </div>
                    </div>
                    <div class="chat-input">
                        <input type="text" id="chat-input" placeholder="Type your message..." disabled>
                        <button id="send-button" onclick="sendMessage()" disabled>Send</button>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>📚 API Documentation</h2>
                <p>Visit <a href="/docs" target="_blank">/docs</a> for interactive API documentation.</p>
            </div>
        </div>
        
        <script>
            let ws = null;
            let personalities = [];
            
            // Initialize WebSocket connection
            function initWebSocket() {
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = `${protocol}//${window.location.host}/ws/chat`;
                
                ws = new WebSocket(wsUrl);
                
                ws.onopen = function() {
                    updateStatus('Connected', true);
                    document.getElementById('chat-input').disabled = false;
                    document.getElementById('send-button').disabled = false;
                };
                
                ws.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    
                    if (data.type === 'chat_response') {
                        addMessage(data.response, 'bot');
                    } else if (data.type === 'error') {
                        addMessage(`Error: ${data.message}`, 'bot');
                    }
                };
                
                ws.onclose = function() {
                    updateStatus('Disconnected', false);
                    document.getElementById('chat-input').disabled = true;
                    document.getElementById('send-button').disabled = true;
                    
                    // Reconnect after 3 seconds
                    setTimeout(initWebSocket, 3000);
                };
                
                ws.onerror = function(error) {
                    console.error('WebSocket error:', error);
                    updateStatus('Error', false);
                };
            }
            
            function updateStatus(text, connected) {
                const statusElement = document.getElementById('status');
                const statusText = document.getElementById('status-text');
                
                statusText.textContent = text;
                statusElement.className = connected ? 'status connected' : 'status disconnected';
            }
            
            function addMessage(message, sender) {
                const messagesContainer = document.getElementById('chat-messages');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}-message`;
                
                if (sender === 'user') {
                    messageDiv.innerHTML = `<strong>You:</strong> ${message}`;
                } else {
                    messageDiv.innerHTML = `<strong>AI:</strong> ${message}`;
                }
                
                messagesContainer.appendChild(messageDiv);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
            
            function sendMessage() {
                const input = document.getElementById('chat-input');
                const message = input.value.trim();
                
                if (message && ws && ws.readyState === WebSocket.OPEN) {
                    addMessage(message, 'user');
                    
                    ws.send(JSON.stringify({
                        type: 'chat',
                        personality_id: 'default',
                        message: message,
                        provider: 'openai',
                        model: 'gpt-3.5-turbo'
                    }));
                    
                    input.value = '';
                }
            }
            
            // Handle Enter key
            document.getElementById('chat-input').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
            
            // Initialize
            initWebSocket();
        </script>
    </body>
    </html>
    """


# Request/Response models
class CompileRequest(BaseModel):
    personality_data: Dict[str, Any]
    provider: str
    model: Optional[str] = None
    include_metadata: bool = True


class ValidateRequest(BaseModel):
    personality_data: Dict[str, Any]
    strict: bool = False


class BlendRequest(BaseModel):
    personality_weights: Dict[str, float]
    custom_name: Optional[str] = None


class TestRequest(BaseModel):
    personality_data: Dict[str, Any]
    provider: str
    model: Optional[str] = None
    test_message: str = "Hello, how are you?"
