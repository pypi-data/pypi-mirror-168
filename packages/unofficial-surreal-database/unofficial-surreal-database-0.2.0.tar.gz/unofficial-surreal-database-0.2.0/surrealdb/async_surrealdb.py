"""Module to manage a SurrealDB database asynchronously."""
from __future__ import annotations
from typing import Any, List, Optional

import httpx

from surrealdb.error import AuthenticationError, QueryError


class AsyncSurrealDB:
    """Operate on a SurrealDB instance asynchronously."""

    def __init__(
        self,
        username: Optional[str] = "",
        password: Optional[str] = "",
        namespace: Optional[str] = "",
        database: Optional[str] = "",
        url: Optional[str] = "http://localhost:8000/sql",
    ) -> AsyncSurrealDB:
        """
        # AsyncSurrealDB.

        Query a SurrealDB database asynchronously.

        Params:
            username: The username to use for authentication.
            password: The password to use for authentication.
            namespace: The namespace to use.
            database: The database to use.
            url: The URL to the SurrealDB instance.

        Params other than url are optional. You can set them later
        using the `signin`, and `use` methods.
        """
        self.headers = {
            "Content-Type": "application/json",
            "NS": namespace,
            "DB": database,
        }
        self._client = httpx.AsyncClient(
            auth=(username, password),
            headers=self.headers,
        )
        self.url = url

    async def __aenter__(self):
        """Enter the context manager."""
        return self

    async def __aexit__(self, *_):
        """Exit the context manager."""
        await self.close()

    async def signin(self, username: str, password: str) -> None:
        """
        Sign in to a SurrealDB instance.

        Args:
            username: The username to use for authentication.
            password: The password to use for authentication.
        """
        self._client.auth = (username, password)

    async def signup(self, username: str, password: str) -> None:
        """
        Sign up to a SurrealDB instance.

        Args:
            username: The username to use for authentication.
            password: The password to use for authentication.
        """
        self._client.auth = (username, password)

    async def use(self, namespace: str, database: str) -> None:
        """
        Set the namespace and database to use.

        Args:
            namespace: The namespace to use.
            database: The database to use.
        """
        self.headers["NS"] = namespace
        self.headers["DB"] = database
        self._client.headers = self.headers

    async def query(self, query: str) -> List[Any] | None:
        """
        Execute a SurrealQL statement.

        Returns: A list of dictionaries representing rows in the database.
        Raises: SurrealError if the query fails.

        >>> db = SurrealDB()
        >>> db.query("SELECT * FROM users;")
        [
            {'id': 1, 'name': 'John Doe', 'age': 42},
            {'id': 2, 'name': 'Jane Doe', 'age': 36},
        ]
        """
        response = await self._client.post(url=self.url, data=query)

        if response.status_code == 200 and response.json()[0]["status"] == "OK":
            return response.json()[0].get("result", [])

        if response.status_code == 403:
            raise AuthenticationError(response.json())

        raise QueryError(response.json())

    async def select(self, target: str) -> List[Any]:
        """
        Select all rows from a table.

        Args:
            target: The table to select from.

        Returns: A list of dictionaries representing rows in the database.
        Raises: SurrealError if the query fails.

        >>> db = SurrealDB()
        >>> db.select("users")
        [
            {'id': 1, 'name': 'John Doe', 'age': 42},
            {'id': 2, 'name': 'Jane Doe', 'age': 36},
        ]
        """
        query = f"SELECT * from {target};"
        return await self.query(query)

    async def create(self, target: str, **kwargs: Any) -> List[Any]:
        """
        Create a new row in a table.

        Args:
            target: The table to insert into.
            kwargs: The values to insert.
                Key: The column name.
                Value: The value to insert.

        Returns: A list of dictionaries representing rows in the database.
        Raises:
            ValueError: If no values are provided.
            SurrealError: If the query fails.

        >>> db = SurrealDB()
        >>> db.create("users:1", name="John Doe", age=42)
        [{'id': 1, 'name': 'John Doe', 'age': 42}]
        """
        if not kwargs:
            raise ValueError("Must set at least one value.")

        query = self.__append_kwargs(f"CREATE {target} SET ", **kwargs)

        return await self.query(f"{query};")

    async def change(self, target: str, **kwargs: Any) -> List[Any]:
        """
        Update a row in a table.

        Args:
            target: The table to update.
            kwargs: The values to update.
                Key: The column name.
                Value: The value to update.

        Returns: A list of dictionaries representing rows in the database.
        Raises:
            ValueError: If no values are provided.
            SurrealError: If the query fails.

        >>> db = SurrealDB()
        >>> db.select("users:1")
        [{'id': 1, 'name': 'John Doe', 'age': 42}]
        >>> db.change("users:1", name="Jane Doe")
        [{'id': 1, 'name': 'Jane Doe', 'age': 42}]
        """
        if not kwargs:
            raise ValueError("Must update at least one value.")

        query = self.__append_kwargs(f"UPDATE {target} SET ", **kwargs)

        return await self.query(f"{query};")

    async def delete(self, target: str, where: str = None) -> List[Any]:
        """
        ## Delete an entity from the database.

        Args:
            target: The entity to delete. Can be a row id or a table name.
            where: A condition to filter the rows to delete.

        Returns: A list of dictionaries representing rows in the database.
        Raises: SurrealError if the query fails.

        ### Delete a row by id.
        >>> db = SurrealDB()
        >>> db.select("users")
        [
            {'id': 1, 'name': 'John Doe', 'age': 42},
            {'id': 2, 'name': 'Jane Doe', 'age': 36},
        ]
        >>> db.delete("users:1")
        []
        >>> db.select("users")
        [{'id': 2, 'name': 'Jane Doe', 'age': 36}]

        ### Delete all rows matching a condition.
        >>> db = SurrealDB()
        >>> db.select("users")
        [
            {'id': 1, 'name': 'John Doe', 'age': 42},
            {'id': 2, 'name': 'Jane Doe', 'age': 36},
        ]
        >>> db.delete("users", where="age > 40")
        []
        >>> db.select("users")
        [{'id': 2, 'name': 'Jane Doe', 'age': 36}]

        ### Delete a table.
        >>> db = SurrealDB()
        >>> db.select("users")
        [
            {'id': 1, 'name': 'John Doe', 'age': 42},
            {'id': 2, 'name': 'Jane Doe', 'age': 36},
        ]
        >>> db.delete("users")
        []
        >>> db.select("users")
        []
        """
        query = f"DELETE {target} "

        if where:
            query += f"WHERE {where}"

        return await self.query(f"{query};")

    @staticmethod
    def __append_kwargs(query: str, **kwargs: Any) -> str:
        """Convert keyword arguments to a SurrealQL statement."""
        for key, value in kwargs.items():
            if isinstance(value, str):
                value = f"'{value}'"
            query += f"{key} = {value}, "

        return query[:-2]

    async def close(self):
        """Close the connection to the database."""
        await self._client.aclose()
