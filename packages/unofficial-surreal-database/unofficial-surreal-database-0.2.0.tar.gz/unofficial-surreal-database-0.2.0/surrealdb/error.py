"""Module for SurrealDB exceptions."""
from __future__ import annotations


class SurrealError(Exception):
    """Base class for all SurrealDB exceptions."""


class QueryError(SurrealError):
    """Exception for errors in queries."""


class AuthenticationError(SurrealError):
    """Exception for authentication errors."""
