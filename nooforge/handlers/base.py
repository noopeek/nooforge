from typing import Dict, Callable

HANDLERS: Dict[str, Callable] = {}

def register_handler(name: str):
    def decorator(func):
        HANDLERS[name] = func
        return func
    return decorator

def get_handler(name: str):
    return HANDLERS.get(name)

def list_handlers() -> list:
    return list(HANDLERS.keys())
