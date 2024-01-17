from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from scr.core.repo import BaseRepo
from scr.models import TGSession, LoginStatus


class SessionRepo(BaseRepo):
    model: TGSession

    async def get_one_by_phone(
        self, phone: str, session: AsyncSession
    ) -> TGSession | None:
        return (await session.execute(
            select(self.model).where(self.model.phone == phone))
        ).scalar_one_or_none()

    async def create_one(
        self, phone: str, qr_login_url: str, session: AsyncSession
    ):
        now = datetime.now()
        db_obj = TGSession(
            created_at=now, updated_at=now,
            login_status=LoginStatus.CONFIRM.value,
            phone=phone, qr_login_url=qr_login_url
        )
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update_login_status(
        self, tg_session: TGSession, status: LoginStatus,
        session: AsyncSession
    ) -> TGSession:
        tg_session.login_status = status.value
        tg_session.updated_at = datetime.now()
        session.add(tg_session)
        await session.commit()
        await session.refresh(tg_session)
        return tg_session

    async def update_qr_login_url(
        self, tg_session: TGSession, qr_login_url: str, session: AsyncSession
    ):
        tg_session.qr_login_url = qr_login_url
        tg_session.login_status = LoginStatus.CONFIRM.value
        tg_session.updated_at = datetime.now()
        session.add(tg_session)
        await session.commit()
        await session.refresh(tg_session)
        return tg_session


session_repo = SessionRepo(TGSession)
