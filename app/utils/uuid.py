from uuid import uuid4

def generate() -> str:
    entity = uuid4()
    return f"{entity}"
