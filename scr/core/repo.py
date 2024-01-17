from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepo:

    def __init__(self, model):
        self.model = model

    async def get_one(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_many(
            self,
            session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create_one(
            self,
            obj_in: BaseModel,
            session: AsyncSession
    ):
        obj_in_data = obj_in.model_dump()
        obj_in_data['created_at'] = datetime.now()
        obj_in_data['updated_at'] = datetime.now()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
