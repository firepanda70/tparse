from datetime import datetime

from sqlalchemy.orm import (
    declared_attr, Mapped, mapped_column, DeclarativeBase,
    sessionmaker
)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from .config import settings

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


class BaseDBModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


BaseDBModel.metadata.naming_convention = POSTGRES_INDEXES_NAMING_CONVENTION

engine = create_async_engine(settings.db_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
