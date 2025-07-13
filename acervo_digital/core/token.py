from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from acervo_digital.core.database import  get_db
from acervo_digital.core.security import Auth2

router = APIRouter(tags=['security'])


@router.post('/token')
def login(
    form_user: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    auth = Auth2(db=db)
    access_token = auth.create_access_token(form_user)

    return {"access_token": access_token['access_token'], 'token_type': 'bearer'}
