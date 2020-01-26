import os
import environ

env = environ.Env.read_env()

POSTGRES_ADDRESS = os.getenv("POSTGRES_ADDRESS")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_USERNAME = os.environ.get("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DBNAME = os.environ.get("POSTGRES_DBNAME")
API_KEY = os.environ.get("API_KEY")
