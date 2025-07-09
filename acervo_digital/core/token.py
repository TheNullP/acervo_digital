from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from acervo_digital.core.database import  get_db
from acervo_digital.core.security import Auth2

router = APIRouter(tags=['security'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post('/token')
def login(
    form_user: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    auth = Auth2(db=db)
    auth2 = auth.verifyInDB(form_user)

    return {"access_token": auth2.password, 'token_type': 'bearer'}
