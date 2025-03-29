"""
Tia Interpreter
===============

AI Interpreter Agent: CoPA

A natural language interface for my Windows OS.

Basic Usage
----------
>>> from interpreter import Interpreter
>>> interpreter = Interpreter()
>>> interpreter.chat("Hello, what can you help me with?")

Configuration
------------
>>> from interpreter import Interpreter, Profile

# Load profile
config = interpreter\profiles.py
"""

# Use lazy imports to avoid loading heavy modules immediately
from importlib import import_module


def __getattr__(name):
    """Lazy load attributes only when they're actually requested"""
    if name in ["Interpreter", "Profile"]:
        if name == "Interpreter":
            return getattr(import_module(".interpreter", __package__), name)
        else:
            return getattr(import_module(".profiles", __package__), name)
    raise AttributeError(f"module '{__package__}' has no attribute '{name}'")


__all__ = ["Interpreter", "Profile"]

__version__ = "0.1.0"
