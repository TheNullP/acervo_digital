from fastapi import FastAPI
from fastapi.responses import JSONResponse
from acervo_digital.routers import user


app = FastAPI()

app.include_router(user.router)

@app.get('/')
def get_root():
    return JSONResponse(content={'msg':'Hello World.'})

