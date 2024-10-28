import urllib.parse

from fastapi import APIRouter, Request
from pydantic import BaseModel

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse

# from app.routes.load_model import Model
# from app.routes.model import generate_answer


router = APIRouter()
templates = Jinja2Templates(directory="templates")

class Query(BaseModel):
    model_type: str
    query: str


@router.get("/main")
def hello(request: Request):
    return templates.TemplateResponse(
        name="user_info.html",
        request=request
    )


@router.get("/", response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse(
        name="main.html",
        request=request
    )


# @router.post("/send_query", response_class=HTMLResponse)
# def send_query(request: Request, data: Query):

#     model_type = Model(data.model_type).get_model_type()
#     print("모델 타입:", model_type)
    
#     request_data = {
#         'prompt': data.query,
#         'model_type': model_type,
#     }

#     answer, picture = generate_answer(request_data)
#     print(f"답변: {answer}, 사진: {picture}")

#     json_data = {
#         'answer': answer,
#         'picture': picture
#     }

#     return JSONResponse(content=json_data)