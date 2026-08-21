# Common utilities
def generate_id(prefix: str = "") -> str:
    import uuid
    return f"{prefix}{uuid.uuid4().hex[:8]}"
