from enum import StrEnum

from sqlalchemy.orm import mapped_column, Mapped

from scr.core.db import BaseDBModel


class LoginStatus(StrEnum):
    LOGINED = 'logined'
    CONFIRM = 'waiting_qr_login'
    ERROR = 'error'


class TGSession(BaseDBModel):
    phone: Mapped[str] = mapped_column(unique=True)
    login_status: Mapped[str]
    qr_login_url: Mapped[str | None]
