from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/_ajax/flot_chart_data.json")
async def flot_chart_data():
    data = [
        {
            "label": "당뇨",
            "color": "black",
            "data": [
                [1, 0],
                [2, 0],
                [3, 0],
                [4, 7881],
                [5, 17168],
                [6, 18596],
                [7, 27374],
                [8, 19294],
                [9, 0],
                [10, 0],
                [11, 0],
                [12, 0]
            ],
        },
        {
            "label": "고혈압",
            "color": "pink",
            "data": [
                [1, 0],
                [2, 0],
                [3, 0],
                [4, 7881],
                [5, 7168],
                [6, 8596],
                [7, 7374],
                [8, 9294],
                [9, 0],
                [10, 0],
                [11, 3000],
                [12, 0]
            ],
        },
    ]
    return JSONResponse(content=data)