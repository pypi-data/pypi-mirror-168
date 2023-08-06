# surreal-db-python

A pure python (and compilable) database client for SurrealDB.

## Installation

1. Install with

```bash
pip install surreal-db-python
```

## Usage

```py
import surreal

client = surreal.SurrealDB(
    host: str,
    username: str,
    password: str,
    db: str,
    namespace: str
)

client.execute("CREATE deez:nut SET nice = 69 + 420;")
client.fetch("SELECT * FROM deez:nut;")
```

## Features

- Supported Asynchronous Operation (with class `AsyncSurrealDB`) (`AsyncSurrealDB` have same API as `SurrealDB but you await them.)
- (not) Supported websocket (yet)

## Build from source

1. Clone repository

2. `poetry install`

3. `./setup.py sdist bdist_wheel` for wheel or `./setup.py install` for install package directly (egg included)
