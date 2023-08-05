# SurrealDB Python client library.
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Pypi Version](https://img.shields.io/pypi/v/unofficial-surreal-database)](https://pypi.org/project/unofficial-surreal-database/)

An unofficial client library for SurrealDB using `httpx`.

## Installation
```bash
pip install unofficial-surreal-database
```

## API
This library includes a `SurrealDB` class that can be used to interact with the SurrealDB server.

### `SurrealDB`
The `SurrealDB` class is the main class for interacting with the SurrealDB server. Additionally, `AsyncSurrealDB`, uses the same API as `SurrealDB`, but uses `httpx.AsyncClient` instead of `httpx.Client`. This is useful for asynchronous applications.

Both classes can be instantiated with the following arguments:

- `username` (str): The username to use when connecting to the server.
- `password` (str): The password to use when connecting to the server.
- `namespace` (str): The namespace to query.
- `database` (str): The database to query.
- `url` (str): The URL to connect to. Defaults to `http://localhost:8000/sql` (the default port for SurrealDB).

The `SurrealDB` class can be used as a context manager, which will automatically close the `httpx.Client` connection when the context is exited.

The `SurrealDB` class has the following methods:


#### `SurrealDB.signin`
Signs in to the SurrealDB server. This method can be used to sign in to the server if the `SurrealDB` instance was instantiated without a username and password.

```python
from surrealdb import SurrealDB


with SurrealDB() as db:
    db.signin(username="root", password="root")
```

#### `SurrealDB.signup`
Same as `SurrealDB.signin`.


#### `SurrealDB.use`
Sets the namespace and database to use for queries.

```python
from surrealdb import SurrealDB


with SurrealDB() as db:
    db.use(namespace="my_namespace", database="my_database")
```

#### `SurrealDB.query`
Queries the SurrealDB server.

```python
from surrealdb import SurrealDB


with SurrealDB() as db:
    db.signin(username="root", password="root")
    db.use(namespace="my_namespace", database="my_database")
    result = db.query("SELECT * FROM users")

    >>> result
    [
        {
            "id": 1,
            "name": "John Doe",
        },
        {
            "id": 2,
            "name": "Jane Doe",
        }
    ]

```


#### `SurrealDB.select`
Wrapper on `SurrealDB.query` that allows you to select a table, or record from a table.

```python
from surrealdb import SurrealDB


with SurrealDB() as db:
    db.signin("root", "root")
    db.use("test", "test")

    result = db.select("users")
    >>> result
    [
        {
            "id": 1,
            "name": "John Doe",
        },
        {
            "id": 2,
            "name": "Jane Doe",
        }
    ]

    result = db.select("users:2")
    >>> result
    [
        {
            "id": 2,
            "name": "Jane Doe",
        }
    ]
```


#### `SurrealDB.create`

Create a record in the database.

Takes keyword arguments for the record to create, and a first parameter as the record, or record and identifier.

```python
from surrealdb import SurrealDB


with SurrealDB() as db:
    db.signin("root", "root")
    db.use("test", "test")

    result = db.create("users:1", name="John Doe")
    >>> result
    [
        {
            "id": 1,
            "name": "John Doe",
        }
    ]
```


#### `SurrealDB.change`

Change a record in the database.

Takes keyword arguments for the record to change, and a first parameter as the record and identifier.

```python
from surrealdb import SurrealDB


with SurrealDB() as db:
    db.signin("root", "root")
    db.use("test", "test")

    result = db.change("users:1", age=42)
    >>> result
    [
        {
            "id": 1,
            "name": "John Doe",
            "age": 42,
        }
    ]
```



#### `SurrealDB.delete`

Delete a record in the database.

Takes a first parameter as the record and identifier, with an optional `where` parameter, to delete all items that match the where clause.

```python
from surrealdb import SurrealDB


with SurrealDB() as db:
    db.signin("root", "root")
    db.use("test", "test")

    result = db.delete("users", where="age > 40")
    >>> result
    []
```

#### `SurrealDB.close`

Manually close the `httpx.Client` connection. This is done for you when using the `SurrealDB` class as a context manager.


### `Reference`
The `Reference` class is used to represent a reference to a record in the database. It can be instantiated with the following arguments:

- `table` (str): The table the record exists in.
- `record_id` (str): The record identifier.

The `Reference` class has no methods for ease of use.

```python
from surrealdb import Reference, SurrealDB


with SurrealDB() as db:
    db.signin("root", "root")
    db.use("test", "test")

    db.create("category:work", name="Work")
    db.create(
        "note:1", 
        title="Meeting", 
        category=Reference("category", "work"),
    )

    result = db.query(
        """
        SELECT * 
        FROM 
            note 
        WHERE 
            category = category:work 
        FETCH 
            category;
        """
    )

    >>> result
    [
        {
            "category": {
                "id": "category:work", 
                "name": "Work"
                }, 
            "id": "note:1", 
            "title": "Meeting"
        }
    ]
