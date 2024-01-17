from pydantic import BaseModel


class LoginSchema(BaseModel):
    phone: str
