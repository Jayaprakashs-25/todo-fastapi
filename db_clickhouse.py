import clickhouse_connect
import os
from dotenv import load_dotenv

load_dotenv()

client = clickhouse_connect.get_client(
    host = os.getenv("CLICKHOUSE_HOST"),
    port = int(os.getenv("CLICKHOUSE_PORT")),
    username = os.getenv("CLICKHOUSE_USER"),
    password = os.getenv("CLICKHOUSE_PASSWORD"),
    database = os.getenv("CLICKHOUSE_DATABASE"),
    secure=True
)

