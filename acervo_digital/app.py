from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from acervo_digital.routers import user, book
from acervo_digital.core import token
from acervo_digital.core.token import oauth2_scheme



app = FastAPI()

app.include_router(user.router)
app.include_router(book.router)
app.include_router(token.router)



@app.get('/')
def get_root(token: Annotated[str, Depends(oauth2_scheme)]):
    return JSONResponse(content={'msg':'Hello World.'})

@app.get('/auth')
async def auth(token: Annotated[str, Depends(oauth2_scheme)]):
    return {'token': token}
