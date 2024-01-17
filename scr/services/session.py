from asyncio import TimeoutError

from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from telethon import TelegramClient
from telethon.custom import QRLogin
from telethon.errors import SessionPasswordNeededError

from scr.core.config import settings, BASE_DIR
from scr.repos import session_repo
from scr.schemas import LoginSchema, QRLink, StausCheck
from scr.models import TGSession, LoginStatus
from .errors import AlreadyLogined, SessionNotFound, NotAuthorized, PhoneInvalidFormat

SESSIONS_DIR = BASE_DIR / 'tg_sessions'


class SessionService:

    async def generate_client(self, phone: str):
        return TelegramClient(
            str(SESSIONS_DIR / phone),
            settings.api_id, settings.api_hash
        )

    async def login(
        self, login_data: LoginSchema, background_tasks: BackgroundTasks,
        session: AsyncSession
    ) -> QRLink:
        if not login_data.phone.isdigit():
            raise PhoneInvalidFormat
        tg_session = await session_repo.get_one_by_phone(
            login_data.phone, session
        )
        if tg_session:
            if tg_session.login_status == LoginStatus.CONFIRM:
                return QRLink(qr_link_url=tg_session.qr_login_url)
            if tg_session.login_status == LoginStatus.LOGINED:
                raise AlreadyLogined
        client = await self.generate_client(login_data.phone)
        await client.connect()
        qr_login = await client.qr_login()
        if not tg_session:
            tg_session = await session_repo.create_one(
                login_data.phone, qr_login.url, session
            )
        else:
            tg_session = await session_repo.update_qr_login_url(
                tg_session, qr_login.url, session
            )
        background_tasks.add_task(
            self.__wait_login, qr_login, tg_session, client, session
        )
        return QRLink(qr_link_url=qr_login.url)

    async def get_one_by_phone(self, phone: str, session: AsyncSession):
        if not phone.isdigit():
            raise PhoneInvalidFormat
        tg_session = await session_repo.get_one_by_phone(phone, session)
        if not tg_session:
            raise SessionNotFound
        return tg_session
    
    async def get_authorized(self, phone: str, session: AsyncSession):
        tg_session = await self.get_one_by_phone(phone, session)
        if tg_session.login_status != LoginStatus.LOGINED:
            raise NotAuthorized
        return tg_session

    async def status_check(self, phone: str, session: AsyncSession):
        if not phone.isdigit():
            raise PhoneInvalidFormat
        tg_session = await self.get_one_by_phone(phone, session)
        return StausCheck(status=tg_session.login_status)

    async def __wait_login(
        self, qr_login: QRLogin, tg_session: TGSession,
        client: TelegramClient, session: AsyncSession
    ):
        try:
            await qr_login.wait()
        except (TimeoutError, SessionPasswordNeededError):
            await session_repo.update_login_status(
                tg_session, LoginStatus.ERROR, session
            )
        else:  
            await session_repo.update_login_status(
                tg_session, LoginStatus.LOGINED, session
            )
        finally:
            await client.disconnect()


session_service = SessionService()
