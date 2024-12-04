from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/_ajax/flot_chart_data.json")
async def flot_chart_data():
    diabetes_data = [
        [1, 0.14], [2, 0.19], [3, 0.27], [4, 0.57],
        [5, 0.80], [6, 1.23], [7, 1.70], [8, 2.11],
        [9, 2.50], [10, 2.99], [11, 3.15], [12, 3.34],
        [13, 3.23], [14, 3.20]
    ]

    hypertension_data = [
        [1, 34.19], [2, 44.30], [3, 55.83], [4, 62.62],
        [5, 61.13], [6, 65.15], [7, 68.95], [8, 67.98],
        [9, 63.09], [10, 57.12], [11, 53.99], [12, 51.58],
        [13, 50.27], [14, 52.19]
    ]

    dyslipidemia_data = [
        [1, 47.54], [2, 50.08], [3, 53.23], [4, 57.26],
        [5, 52.01], [6, 56.37], [7, 59.60], [8, 63.00],
        [9, 68.25], [10, 74.21], [11, 77.66], [12, 80.08],
        [13, 80.99], [14, 77.87]
    ]

    obesity_data = [
        [1, 14.70], [2, 18.31], [3, 23.50], [4, 26.15],
        [5, 21.01], [6, 19.82], [7, 20.56], [8, 22.03],
        [9, 25.79], [10, 30.44], [11, 33.53], [12, 35.73],
        [13, 35.59], [14, 29.89]
    ]

    data = [
        {"label": "당뇨", "color": "red", "data": diabetes_data},
        {"label": "고혈압", "color": "pink", "data": hypertension_data},
        {"label": "이상지질혈증", "color": "black", "data": dyslipidemia_data},
        {"label": "복부비만", "color": "brown", "data": obesity_data}
    ]

    return JSONResponse(content=data)
