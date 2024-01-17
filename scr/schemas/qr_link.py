from pydantic import BaseModel


class QRLink(BaseModel):
    qr_link_url: str
