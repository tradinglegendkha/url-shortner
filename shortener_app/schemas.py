#this schema file states what this API expects as a request body
from pydantic import BaseModel

class URLBase(BaseModel):
    target_url: str

class URL(URLBase):
    is_active: bool
    clicks: int 

    class Configt:
        orm_mode = True

class URLInfo(URL):
    url: str
    admin_url: str 