from zoneinfo import ZoneInfo
from datetime import datetime, timedelta, timezone
import jwt
from fastapi.exceptions import HTTPException
from passlib.context  import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends


from acervo_digital.core.database import User, get_db
from acervo_digital.core.settings import Settings
from fastapi.security import OAuth2PasswordBearer
from acervo_digital.schemas.token_schema import UserToken
from acervo_digital.schemas.user_schema import UserSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
settings = Settings()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM =  settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES



def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

class Auth2:
    def __init__(self, db: Session):
        self.db = db

    def create_access_token(
        self,
        user: UserSchema,
        exp: int = ACCESS_TOKEN_EXPIRE_MINUTES 
    ):
        userDB = self.db.query(User).filter_by(username=user.username).first()
        if not userDB:
            raise HTTPException(
                detail='Usuário ou senha Incorreto.',
                status_code=401
            )

        auth = verify_password(user.password, userDB.password)
        if not auth:
            raise HTTPException(
                detail='Usuário ou senha Incorreto.',
                status_code=401
            )

        expire =  datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=int(exp))
        payload ={'sub': userDB.username, 'exp': expire}

        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {'access_token': encoded_jwt, 'token_type': 'Bearer'}

    def verify_token(self, access_token: str,):
        try:
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])

            user = payload.get('sub')
            if user is None:
                raise HTTPException(
                    detail=''
                )

            userDB = self.db.query(User).filter_by(username=user).first()

            if not userDB:
                raise HTTPException(
                    detail='Usuário não localizado.',
                    status_code=404
                )

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                detail='Token expirado!',
                status_code=401
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                detail=f'Token Invalido!',
                status_code=401
            )
        except Exception as e:
            raise e

        return userDB



def verify(
    db: Session = Depends(get_db),
    access_token: str = Depends(oauth2_scheme),
):
    if access_token is None:
        raise HTTPException(detail='Token vazio.', status_code=401)

    auth = Auth2(db=db)
    auth_token = auth.verify_token(access_token=access_token)
    authUser = UserToken(
        id=auth_token.id,
        username=auth_token.username
    )

    return authUser
