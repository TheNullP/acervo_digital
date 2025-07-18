from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str

class UserToken(BaseModel):
    id: int
    username: str
