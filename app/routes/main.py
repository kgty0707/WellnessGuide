from fastapi import APIRouter, Request, Form, HTTPException
from pydantic import BaseModel, EmailStr, Field

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.routes.shop import search_product

# from app.routes.load_model import Model
from app.model.model import model
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
def receive_user_detail_info(request: Request,
                             name: str = Form(...),
                             gender: str = Form(...),
                             age: str = Form(...),
                             height: str = Form(...),
                             weight: str = Form(...),
                             systolic: str = Form(...),
                             diastolic: str = Form(...),
                             fasting_glucose: str = Form(...),
                             waist_circumference: str = Form(...),
                             total_cholesterol: str = Form(...),
                             hdl_cholesterol: str = Form(...),
                             ldl_cholesterol: str = Form(...),
                             triglycerides: str = Form(...)):
    user_data = {
        "name": name,
        "gender": gender,
        "age": age,
        "height": height,
        "weight": weight,
        "systolic": systolic,
        "diastolic": diastolic,
        "fasting_glucose": fasting_glucose,
        "waist_circumference": waist_circumference,
        "total_cholesterol": total_cholesterol,
        "hdl_cholesterol": hdl_cholesterol,
        "ldl_cholesterol": ldl_cholesterol,
        "triglycerides": triglycerides,
    }

    print(user_data)

    # Probabilities: {'당뇨': 20, '고혈압': 30, '비만': 32, '이상지질혈증': 18}
    probabilities = calculate_disease_probabilities(
        gender=user_data["gender"],
        systolic=int(user_data["systolic"]),
        diastolic=int(user_data["diastolic"]),
        fasting_glucose=int(user_data["fasting_glucose"]),
        waist_circumference=int(user_data["waist_circumference"]),
        total_cholesterol=float(user_data["total_cholesterol"]),
        hdl_cholesterol=float(user_data["hdl_cholesterol"]),
        ldl_cholesterol=float(user_data["ldl_cholesterol"]),
        triglycerides=float(user_data["triglycerides"])
    )

    print(f"Probabilities:")
    print(probabilities)

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

    recommended_counts = recommend_products(risk_levels)

    recommend_shop_counts = recommend_shop_products(risk_levels)

    products = search_product(recommend_shop_counts)

    recommendations = {}
    for disease, top_k in recommended_counts.items():
        query_text = disease
        recommendations[disease] = search_by_main_fnctn(query_text, top_k=top_k)


    return templates.TemplateResponse(
        name="send_info.html",
        request=request,
        context={
            "request": request,
            "user_info": user_data,
            "probabilities": probabilities,
            "risk_levels": risk_levels,
            "recommendations": recommendations,
            "average_probability": average_probability,
            "overall_risk_level": overall_risk_level,
            "overall_message": overall_message,
            "products": products
        }
    )


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
        print(f"User Info: {user_info}")

        input_data = {
            "성별": int(gender),
            "연령대코드": int(age),
            "신장": float(height),
            "체중": float(weight),
            "수축기 혈압": float(systolic),
            "이완기 혈압": float(diastolic)
        }

        print(f"Input Data Info: {input_data}")

        probabilities = model(input_data)
        print(f"Probabilities: {probabilities}") 

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

        recommended_counts = recommend_products(risk_levels)

        recommend_shop_counts = recommend_shop_products(risk_levels)

        products = search_product(recommend_shop_counts)

        recommendations = {}
        for disease, top_k in recommended_counts.items():
            query_text = disease
            recommendations[disease] = search_by_main_fnctn(query_text, top_k=top_k)

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
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail="데이터 처리에 실패했습니다.")


def calculate_disease_probabilities(gender: str,
                                    systolic: int,
                                    diastolic: int,
                                    fasting_glucose: int,
                                    waist_circumference: int,
                                    total_cholesterol: float,
                                    hdl_cholesterol: float,
                                    ldl_cholesterol: float,
                                    triglycerides: float) -> dict:
    """
    입력값에 따라 규칙 기반으로 연속적인 확률(회귀값)을 계산하며,
    각 값을 소수점 셋째 자리에서 반올림하고 백분위로 변환합니다.

    Args:
        gender (str): 성별 (남자/여자)
        systolic (int): 수축 혈압
        diastolic (int): 이완 혈압
        fasting_glucose (int): 공복 혈당
        waist_circumference (int): 허리 둘레
        total_cholesterol (float): 총 콜레스테롤
        hdl_cholesterol (float): HDL 콜레스테롤
        ldl_cholesterol (float): LDL 콜레스테롤
        triglycerides (float): 트리글리세라이드

    Returns:
        dict: 각 질병의 백분위 확률
    """
    probabilities = {}
     # Probabilities: {'당뇨': 20, '고혈압': 30, '비만': 32, '이상지질혈증': 18}
    # 당뇨 (Diabetes)
    if fasting_glucose >= 126:
        probabilities["당뇨"] = 100.0  # 126 이상일 경우 100%
    elif fasting_glucose >= 100:
        probabilities["당뇨"] = round((fasting_glucose - 100) / 26 * 100, 1)  # 100~125 사이
    else:
        probabilities["당뇨"] = round(fasting_glucose / 100 * 100, 1)  # 100 미만


    # 고혈압 (Hypertension)
    systolic_ratio = max(0, (systolic - 130) / 50) if systolic >= 130 else 0
    diastolic_ratio = max(0, (diastolic - 85) / 50) if diastolic >= 85 else 0
    probabilities["고혈압"] = round(min(1.0, systolic_ratio + diastolic_ratio) * 100, 1)

    # 복부비만 (Abdominal Obesity)
    waist_threshold = 90 if gender.lower() == "1" else 85

    if waist_circumference >= waist_threshold:
        probabilities["복부비만"] = 100.0  # 기준 이상은 100%
    else:
        probabilities["복부비만"] = round(waist_circumference / waist_threshold * 100, 1)  # 기준 미만은 비율 계산


    # 이상지질혈증 (Dyslipidemia)
    total_cholesterol_prob = round(
        (min(1.0, (total_cholesterol - 200) / 100) if total_cholesterol >= 200 else total_cholesterol / 200) * 100, 1
    )
    ldl_cholesterol_prob = round(
        (min(1.0, (ldl_cholesterol - 130) / 70) if ldl_cholesterol >= 130 else ldl_cholesterol / 130) * 100, 1
    )
    hdl_cholesterol_prob = round(
        (min(1.0, (40 - hdl_cholesterol) / 20) if hdl_cholesterol <= 40 else 
         (60 - hdl_cholesterol) / 20 if hdl_cholesterol <= 60 else 0) * 100, 1
    )
    triglycerides_prob = round(
        (min(1.0, (triglycerides - 150) / 100) if triglycerides >= 150 else triglycerides / 150) * 100, 1
    )

    # 최대값 계산
    max_probability = max(total_cholesterol_prob, ldl_cholesterol_prob, hdl_cholesterol_prob, triglycerides_prob)
    probabilities["이상지질혈증"] = max_probability

    # 결과 출력
    print(probabilities)
    return probabilities
