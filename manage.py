from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.common.util import register

def create_app():
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="static"), name="static")
    register(app, 'app.routes.main')
    return app


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("manage:create_app", host="localhost", port=8000, reload=True, factory=True)