from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from acervo_digital.core.database import User, get_db
from acervo_digital.core.security import verify_password
from acervo_digital.schemas.user_schema import UserSchema
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(tags=['security'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post('/token')
def login(
    form_user: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    auth = db.query(User).filter_by(username=form_user.username).first()

    if not auth:
        raise HTTPException(
            detail='Usuário ou senha incorreto.',
            status_code=401
        )

    token = verify_password(form_user.password, auth.password)

    if not token:
        raise HTTPException(
            detail='Token invalido.',
            status_code=401
        )

    return {"access_token": form_user.password, 'token_type': 'bearer'}
