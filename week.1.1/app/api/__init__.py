"""
API package initializer

This file exposes the main FastAPI router so it can be imported as:
    from app.api import router
"""

from .routes import router

__all__ = ["router"]
