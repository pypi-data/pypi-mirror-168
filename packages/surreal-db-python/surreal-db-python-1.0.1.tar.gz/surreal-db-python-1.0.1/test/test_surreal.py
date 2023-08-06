import sys
sys.path.append("..")
import surreal
from dotenv import Dotenv

import os

env = Dotenv("../.env")

client = surreal.SurrealDB(env["surreal_host"], env["surreal_username"],env["surreal_password"],env["surreal_database"],env["surreal_namespace"])
async_client = surreal.AsyncSurrealDB(env["surreal_host"], env["surreal_username"],env["surreal_password"],env["surreal_database"],env["surreal_namespace"])
def test_create():
    return (client.execute("CREATE deez;"))
async def test_async():
    return (await async_client.execute("CREATE nut;"))