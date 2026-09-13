class AAFException(Exception):
    """Base exception for AAF."""
    pass

class AgentError(AAFException):
    pass

class ConfigurationError(AAFException):
    pass

class SkillError(AAFException):
    pass

class ValidationError(AAFException):
    pass

class ExecutionError(AAFException):
    pass
