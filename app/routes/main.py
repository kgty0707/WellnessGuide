from fastapi import FastAPI, APIRouter, Request, Form, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse

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
        # 데이터 처리 로직 추가 (예: 데이터베이스 저장)
        user_info = {
            "name": name,
            "height": height,
            "weight": weight,
            "phone": phone
        }
        print(user_info)  # 디버깅용 출력

        # 제출 완료 페이지 렌더링
        return templates.TemplateResponse(
            name="send_info.html",
            request=request,
            context={"request": request, "user_info": user_info}
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="데이터 처리에 실패했습니다.")

@router.get("/send_info", response_class=HTMLResponse)
def send_info(request: Request):
    return templates.TemplateResponse(
        name="send_info.html",
        request=request
    )