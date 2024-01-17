from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from scr.core.db import get_async_session
from scr.schemas import LoginSchema, QRLink, StausCheck, Messages, MessageCreate
from scr.services import session_service, message_service

router = APIRouter()


@router.post('/login')
async def login(
    login_data: LoginSchema,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session)
) -> QRLink:
    return await session_service.login(login_data, background_tasks, session)


@router.get('/check/login')
async def check_login(
    phone: str, session: AsyncSession = Depends(get_async_session)
) -> StausCheck:
    return await session_service.status_check(phone, session)


@router.get('/messages')
async def messages(
    phone: str, uname: str,
    session: AsyncSession = Depends(get_async_session)
) -> Messages:
    return await message_service.get_many(phone, uname, session)

@router.post('/messages')
async def send_message(
    message_data: MessageCreate,
    session: AsyncSession = Depends(get_async_session)
):
    return await message_service.send_message(message_data, session)
