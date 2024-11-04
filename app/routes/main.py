from fastapi import FastAPI, APIRouter, Request, Form, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from app.routes.shop import search_product

# from app.routes.load_model import Model
# from app.routes.model import generate_answer

router = APIRouter()
templates = Jinja2Templates(directory="templates")

class UserInfo(BaseModel):
    name: str = Field(..., min_length=1, description="User's name")
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15, description="User's phone number")



@router.get("/", response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse(
        name="user_info.html",
        request=request
    )


@router.post("/user_info", response_class=HTMLResponse)
def receive_user_info(request: Request,
                      name: str = Form(...),
                      height: str = Form(...),
                      weight: str = Form(...),
                      phone: str = Form(...)):
    try:
        user_info = {
            "name": name,
            "height": height,
            "weight": weight,
            "phone": phone
        }

        products = search_product("당뇨 건강기능식품")

        return templates.TemplateResponse(
            name="send_info.html",
            request=request,
            context={"request": request, "user_info": user_info, "products": products}
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="데이터 처리에 실패했습니다.")


@router.get("/send_info")
def send_info(request: Request):
    return templates.TemplateResponse(
        name="send_info.html",
        request=request
    )
