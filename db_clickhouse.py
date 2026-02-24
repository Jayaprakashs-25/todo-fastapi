import clickhouse_connect
import os
from dotenv import load_dotenv

load_dotenv()

def get_clickhouse_client():
    return clickhouse_connect.get_client(
        host = os.getenv("CLICKHOUSE_HOST"),
        port = 8443,
        username = os.getenv("CLICKHOUSE_USER"),
        password = os.getenv("CLICKHOUSE_PASSWORD"),
        database = os.getenv("CLICKHOUSE_DATABASE"),
        secure=True,
        interface="https"
)
client = get_clickhouse_client()
