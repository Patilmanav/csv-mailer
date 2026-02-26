from pydantic import BaseModel
from typing import List, Optional


class EmailConfig(BaseModel):
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    use_tls: bool = True
    subject: str
    html_body: str
    plain_body: str
    cc: List[str] = []
