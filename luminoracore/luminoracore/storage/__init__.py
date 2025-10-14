"""
Storage module for LuminoraCore Core

Handles database migrations and Core-specific tables.

NOTE: This is separate from SDK's session storage.
- SDK handles: sessions, messages, conversation state
- Core handles: affinity, facts, episodes, moods (personality data)
"""

from .migrations.migration_manager import MigrationManager, MigrationError

__all__ = ['MigrationManager', 'MigrationError']

