from fastapi import APIRouter, Request, Form, HTTPException
from pydantic import BaseModel, EmailStr, Field

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.routes.shop import search_product

# from app.routes.load_model import Model
from app.routes.model import model
from app.routes.medicine import classify_risk, recommend_products, search_by_main_fnctn, calculate_overall_risk, recommend_shop_products

router = APIRouter()
templates = Jinja2Templates(directory="templates")

class UserInfo(BaseModel):
    name: str = Field(..., min_length=1, description="User's name")
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15, description="User's phone number")


@router.get("/", response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse(
        name="main.html",
        request=request
    )


@router.get("/dashboard", response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse(
        name="dashboard.html",
        request=request
    )


@router.post("/user_detail_info", response_class=HTMLResponse)
def receive_user_detail_info():
    pass


@router.post("/user_info", response_class=HTMLResponse)
def receive_user_info(request: Request,
                      name: str = Form(...),
                      gender: str = Form(...),
                      age: str = Form(...),
                      height: str = Form(...),
                      weight: str = Form(...),
                      systolic: str = Form(...),
                      diastolic: str = Form(...)):
    try:
        # 사용자 정보 저장
        user_info = {
            "name": name,
            "gender": gender,
            "age": age,
            "height": height,
            "weight": weight,
            "systolic": systolic,
            "diastolic": diastolic
        }
        print(user_info)  # 디버깅용 출력

        # 모델 확률 값 가져오기
        probabilities = model()

        # 위험도 분류
        risk_levels = {}
        for condition, probability in probabilities.items():
            level, message, color = classify_risk(condition, probability)
            risk_levels[condition] = {
                "probability": probability,
                "level": level,
                "message": message,
                "color": color
            }

        average_probability, overall_risk_level, overall_message = calculate_overall_risk(probabilities)

        # 위험 레벨별 약 추천 개수
        recommended_counts = recommend_products(risk_levels)
        recommend_shop_counts = recommend_shop_products(risk_levels)
        
        # 추천 제품 검색
        products = search_product(recommend_shop_counts)

        # 각 질병별 추천 제품
        recommendations = {}
        for disease, top_k in recommended_counts.items():
            query_text = disease  # 질병명을 query_text로 사용
            recommendations[disease] = search_by_main_fnctn(query_text, top_k=top_k)

        # 템플릿에 전달
        return templates.TemplateResponse(
            name="send_info.html",
            request=request,
            context={
                "request": request,
                "user_info": user_info,
                "probabilities": probabilities,
                "risk_levels": risk_levels,
                "recommendations": recommendations,
                "average_probability": average_probability,
                "overall_risk_level": overall_risk_level,
                "overall_message": overall_message,
                "products": products
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="데이터 처리에 실패했습니다.")