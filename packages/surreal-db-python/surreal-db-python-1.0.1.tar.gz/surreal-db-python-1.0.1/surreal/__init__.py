try:
    from .surreal_compiled import SurrealDB,AsyncSurrealDB
except (ImportError,Exception):
    from .client import SurrealDB,AsyncSurrealDB
