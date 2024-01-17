from pydantic import BaseModel

from scr.models import LoginStatus


class StausCheck(BaseModel):
    status: LoginStatus
