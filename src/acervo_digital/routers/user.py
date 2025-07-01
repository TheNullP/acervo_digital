from typing import Optional
from fastapi import APIRouter, Depends, Form
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from acervo_digital.schemas.user_schema import UserSchema

from acervo_digital.core.database import User, get_db


router = APIRouter(tags=["user"])


@router.get('/readUsers')
def read_users(
    db: Session = Depends(get_db)
):
    users = db.query(User).all()

    return users

@router.post('/createUser')
def create_user(
    username: str,
    password: str,
    db: Session = Depends(get_db)
):
    exists = db.query(User).filter_by(username=username).first()

    if exists:
        raise HTTPException(
            detail={'msg': 'Usuário ou Email já existente.'},
            status_code=400
        )
    new_user = User(
        username=username,
        password=password
    ) 

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return JSONResponse(
        content={'msg':'Usuário criado com sucesso.'},
        status_code=201
    )


@router.put('/updateUser')
def update_user(
    userId: int,
    username: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    exists_user = db.query(User).filter_by(id=userId).first()

    if not exists_user:
        return JSONResponse(
            content={'msg':'Usuário não localizado.'},
            status_code=404
        )
    if username:
        exists_user.username = username
    if password:
        exists_user.password = password

    db.add(exists_user)
    db.commit()
    db.refresh(exists_user)

    return JSONResponse(
        content={ 'msg': 'Atualizado' },
        status_code=200
    )

@router.delete('/deleteUser')
def delete_user(
    userId: int,
    db: Session = Depends(get_db)
):
    exists = db.query(User).filter_by(id=userId).first()

    if not exists:
        raise HTTPException(
            detail={'msg': 'Usuário não localizado.'},
            status_code=404
        )
    db.delete(exists)
    db.commit()

    return JSONResponse(
        content={'msg': 'Deletado com sucesso.'},
        status_code=200
    )
