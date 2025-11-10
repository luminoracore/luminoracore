"""Compilation-related type definitions."""

from __future__ import annotations

from enum import Enum


class CompilationType(str, Enum):
    """Compilation type enumeration."""
    PROMPT = "prompt"
    SYSTEM_MESSAGE = "system_message"
    TEMPLATE = "template"
    CUSTOM = "custom"
