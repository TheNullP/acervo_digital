from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from acervo_digital.core.database import Book, User, get_db


router = APIRouter(tags=["book"])

@router.get('/readBook')
def reade_book(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books

@router.post('/createBook')
def create_book(
    idUser: int,
    title: str,
    author: str,
    db: Session = Depends(get_db)
):
    Exists = db.query(User).filter_by(id=idUser).first()

    if not Exists:
        raise HTTPException(
            detail={'msg':"Usuário não encontrado."},
            status_code=404
        )
    newBook = Book(
        title=title,
        author=author,
        id_user=idUser
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
    db: Session = Depends(get_db),
):
    exists = db.query(Book).filter_by(id=idBook).first()

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
