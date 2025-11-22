"""Conversation-related type definitions."""

from __future__ import annotations

from enum import Enum


class ConversationType(str, Enum):
    """Conversation type enumeration."""
    CHAT = "chat"
    QNA = "qna"
    CREATIVE = "creative"
    ANALYTICAL = "analytical"
