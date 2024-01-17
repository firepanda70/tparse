from telethon.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from scr.core.config import MESSAGE_LIMIT
from scr.schemas.message import (
    Message, Messages, MessageCreate, 
    MessageCreateResponseStatus, MessageCreateResponse
)
from .session import session_service


class MessageService:

    async def get_many(self, phone: str, uname: str, session: AsyncSession):
        await session_service.get_authorized(phone, session)
        client = await session_service.generate_client(phone)
        await client.connect()
        messages = await client.get_messages(uname, MESSAGE_LIMIT)
        await client.disconnect()
        return Messages(
            messages=[
                Message(
                    message_text=message.message, is_self=message.out,
                    username=message._sender.username
                )
                for message in messages
            ]
        )

    async def send_message(
        self, message_data: MessageCreate, session: AsyncSession
    ):
        await session_service.get_authorized(message_data.from_phone, session)
        client = await session_service.generate_client(message_data.from_phone)
        try:
            await client.connect()
            await client.send_message(
                message_data.username, message_data.message_text
            )
            await client.disconnect()
            status = MessageCreateResponseStatus.OK
        except:
            status = MessageCreateResponseStatus.ERROR
        return MessageCreateResponse(status=status)


message_service = MessageService()
