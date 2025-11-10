"""Custom exceptions for LuminoraCore SDK."""


class LuminoraCoreSDKError(Exception):
    """Base exception for all LuminoraCore SDK errors."""
    
    def __init__(self, message: str, error_code: str = None, details: dict = None):
        """
        Initialize the exception.
        
        Args:
            message: Error message
            error_code: Optional error code
            details: Optional additional details
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
    
    def __str__(self) -> str:
        """String representation of the exception."""
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class SessionError(LuminoraCoreSDKError):
    """Exception raised for session-related errors."""
    pass


class ProviderError(LuminoraCoreSDKError):
    """Exception raised for provider-related errors."""
    pass


class PersonalityError(LuminoraCoreSDKError):
    """Exception raised for personality-related errors."""
    pass


class CompilationError(LuminoraCoreSDKError):
    """Exception raised for compilation-related errors."""
    pass


class ValidationError(LuminoraCoreSDKError):
    """Exception raised for validation errors."""
    pass


class ConfigurationError(LuminoraCoreSDKError):
    """Exception raised for configuration errors."""
    pass


class StorageError(LuminoraCoreSDKError):
    """Exception raised for storage-related errors."""
    pass


class AuthenticationError(LuminoraCoreSDKError):
    """Exception raised for authentication errors."""
    pass


class RateLimitError(LuminoraCoreSDKError):
    """Exception raised for rate limit errors."""
    pass


class NetworkError(LuminoraCoreSDKError):
    """Exception raised for network-related errors."""
    pass
