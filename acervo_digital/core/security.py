from fastapi.exceptions import HTTPException
from passlib.context  import CryptContext
from sqlalchemy.orm import Session

from acervo_digital.core.database import User
from acervo_digital.schemas.user_schema import UserSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

class Auth2:
    def __init__(self, db: Session):
        self.db = db

    def verifyInDB(self, user: UserSchema):
        auth_user = self.db.query(User).filter_by(username=user.username).first()

        if not auth_user:
            raise HTTPException(
                detail='Usuário ou senha Incorreto.',
                status_code=401
            )
        
        auth = verify_password(user.password, auth_user.password)

        if not auth:
            raise HTTPException(
                detail='Usuário ou senha Incorreto.',
                status_code=401
            )
        return auth_user

    def create_token_access(self):
        pass
