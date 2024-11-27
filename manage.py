from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.common.util import register
from pathlib import Path
import mimetypes

def create_app():
    app = FastAPI()
    
    mimetypes.init()
    mimetypes.add_type("application/javascript", ".js", strict=True)
    
    BASE_DIR = Path(__file__).parent.resolve()
    static_dir = BASE_DIR / "static"
    
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    
    register(app, 'app.routes.main')
    register(app, 'app.routes.dashboard')
    
    return app

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("manage:create_app", host="localhost", port=8000, reload=True, factory=True)