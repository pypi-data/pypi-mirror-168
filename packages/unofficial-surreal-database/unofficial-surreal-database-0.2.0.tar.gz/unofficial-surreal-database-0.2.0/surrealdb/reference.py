"""Module for referencing data across SurrealDB tables."""
from __future__ import annotations
from typing import Any


class Reference:
    """Reference to another SurrealDB table."""

    def __init__(self, table: str, record_id: Any):
        """
        # SurrealDB Reference.

        Create a reference to another table.

        Params:
            table: The name of the table to reference.
            record_id: The id of the record to reference from that table.
        """
        self.table = table
        self.record_id = record_id

    def __format__(self, format_spec: str) -> str:
        """Format the reference as a string."""
        if format_spec:
            raise NotImplementedError("Format specifiers are not supported.")

        return f"{self.table}:{self.record_id}"
