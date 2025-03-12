import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel, Session
from sqlmodel.ext.asyncio.session import AsyncSession
from appconfig import Settings
import logging
from tenacity import retry, stop_after_attempt, wait_fixed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize engine and sessionmaker once (no globals)
class Database:
    def __init__(self):
        self.engine = None
        self.async_session_maker = None

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(3))
    async def init_db(self):
        settings = Settings()
        self.engine = create_async_engine(
            settings.DATABASE_URL,  # MUST be postgresql+asyncpg://...
            future=True,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
            pool_recycle=3600  # recycle the connections after 1 hour (3600 seconds)
        )
        
        # Test connection
        async with self.engine.begin() as conn:
            await conn.run_sync(lambda _: None)  # Simple connection test
        
        # Create tables
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        
        self.async_session_maker = async_sessionmaker(
            bind=self.engine, 
            expire_on_commit=False
        )

    async def get_db_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_maker() as session:
            yield session

