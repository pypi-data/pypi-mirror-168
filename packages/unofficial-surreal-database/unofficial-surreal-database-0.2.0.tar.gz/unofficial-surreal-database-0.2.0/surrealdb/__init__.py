"""
# SurrealDB client library.

Exports:
    SurrealDB: The SurrealDB client class to query a SurrealDB database.
    Reference: Used to reference a SurrealDB row of a table.
    SurrealQueryError: The error class raised for query errors.
    SurrealAuthenticationError: The error class raised for authentication errors.
"""
from __future__ import annotations


__all__ = [
    "__description__",
    "__title__",
    "__version__",
    "AuthenticationError",
    "AsyncSurrealDB",
    "QueryError",
    "Reference",
    "SurrealDB",
]

from surrealdb.__version__ import __description__, __title__, __version__
from surrealdb.async_surrealdb import AsyncSurrealDB
from surrealdb.error import AuthenticationError, QueryError
from surrealdb.reference import Reference
from surrealdb.surrealdb import SurrealDB
