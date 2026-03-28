from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine: Engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)