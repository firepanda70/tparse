from enum import StrEnum

from pydantic import BaseModel


class Message(BaseModel):
    username: str | None
    is_self: bool
    message_text: str | None


class MessageCreate(BaseModel):
    message_text: str
    from_phone: str
    username: str


class Messages(BaseModel):
    messages: list[Message]


class MessageCreateResponseStatus(StrEnum):
    OK = 'ok'
    ERROR = 'error'


class MessageCreateResponse(BaseModel):
    status: MessageCreateResponseStatus
