from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://neondb_owner:npg_iINRlWH3ty8T@ep-cold-poetry-a1mgtpdm-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()