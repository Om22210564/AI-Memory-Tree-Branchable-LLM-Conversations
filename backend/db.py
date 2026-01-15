from sqlalchemy import create_engine, Table, Column, Integer, MetaData, select
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import Engine
from sqlalchemy import event
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./memory_tree.db")

# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
        "timeout": 30  # ← prevents immediate "database is locked"
    },
    pool_pre_ping=True
)

# Ensure SQLite enforces foreign keys
# @event.listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA journal_mode=WAL")   # ← allow concurrent reads
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Simple schema versioning: increment to force recreate tables when schema changes
SCHEMA_VERSION = 1

def get_schema_version_table(metadata: MetaData):
    return Table(
        "_schema_version",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("version", Integer, nullable=False),
    )

def init_db(drop_if_mismatch: bool = True):
    """Initialize or recreate DB tables. If schema version mismatches, drop and recreate."""
    from . import models

    metadata = Base.metadata
    schema_table = get_schema_version_table(metadata)

    # create schema_version table if missing
    metadata.create_all(bind=engine, tables=[schema_table])
    with engine.begin() as conn:
        result = conn.execute(select(schema_table.c.version)).first()
        if result is None:
            metadata.create_all(bind=engine)
            conn.execute(schema_table.insert().values(version=SCHEMA_VERSION))
        else:
            current = result[0]
            if current != SCHEMA_VERSION:
                if drop_if_mismatch:
                    metadata.drop_all(bind=engine)
                    metadata.create_all(bind=engine)
                    conn.execute(schema_table.delete())
                    conn.execute(schema_table.insert().values(version=SCHEMA_VERSION))
                else:
                    raise RuntimeError("Database schema version mismatch")

    # # check current version
    # with engine.connect() as conn:
    #     result = conn.execute(select(schema_table.c.version)).first()
    #     if result is None:
    #         # fresh DB: create all and set version
    #         metadata.create_all(bind=engine)
    #         conn.execute(schema_table.insert().values(version=SCHEMA_VERSION))
    #     else:
    #         current = result[0]
    #         if current != SCHEMA_VERSION:
    #             if drop_if_mismatch:
    #                 # drop all user tables and recreate
    #                 metadata.drop_all(bind=engine)
    #                 metadata.create_all(bind=engine)
    #                 conn.execute(schema_table.delete())
    #                 conn.execute(schema_table.insert().values(version=SCHEMA_VERSION))
    #             else:
    #                 raise RuntimeError("Database schema version mismatch")
