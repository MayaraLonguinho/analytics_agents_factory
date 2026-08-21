class CoreError(Exception):
    """Base exception for core errors."""
    pass

class ConfigurationError(CoreError):
    pass

class ValidationError(CoreError):
    pass
