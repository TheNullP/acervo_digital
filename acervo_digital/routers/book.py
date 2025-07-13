from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from acervo_digital.core.database import Book, User, get_db
from acervo_digital.core.security import verify


router = APIRouter(tags=["book"])

@router.get('/readBook')
def reade_book(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books

@router.get('/read')
def read_my_book(db: Session = Depends(get_db), Auth_user: Book = Depends(verify)):
    books = db.query(Book).filter_by(id_user=Auth_user.id).all()
    return books


@router.post('/createBook')
def create_book(
    title: str,
    author: str,
    Auth_user: Book = Depends(verify),
    db: Session = Depends(get_db)
):
    Exists = db.query(User).filter_by(id=Auth_user.id).first()

    if not Exists:
        raise HTTPException(
            detail={'msg':"Usuário não encontrado."},
            status_code=404
        )
    newBook = Book(
        title=title,
        author=author,
        id_user=Auth_user.id
    )
    db.add(newBook)
    db.commit()
    db.refresh(newBook)

    return JSONResponse(
        content={'msg':'Livro criado com sucesso.'},
        status_code=201
    )


@router.put('/updateBook')
def update_book(
    idBook: int,
    title: str,
    author: str,
    Auth_user: Book = Depends(verify),
    db: Session = Depends(get_db),
):
    exists = db.query(Book).filter_by(id=Auth_user.id).first()

    if not exists:
        HTTPException(
            detail={'msg':'Livro não localizado.'},
            status_code=404
        )
    try:
        exists.title = title
        exists.author = author

        db.commit()
        db.refresh(exists)
    except Exception as e:
        raise e
    return JSONResponse( 
        content={'msg':'Atualizado com sucesso.'},
        status_code=200
    )



@router.delete('/deleteBook')
def delete_book(
    idBook: int,
    Auth_user: Book = Depends(verify),
    db: Session = Depends(get_db)
):
    exists = db.query(Book).filter_by(id=idBook).first()
    
    if not exists:
        HTTPException(
            detail={'msg':'Livro não localizado.'},
            status_code=404
        )
    try:
        db.delete(exists)
        db.commit()
    except Exception as e:
        raise e

    return JSONResponse(
        content={'msg':'Livro deletado.'},
        status_code=200
    )
