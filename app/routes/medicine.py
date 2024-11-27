from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
INDEX_NAME = os.getenv('INDEX_NAME')

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

QUERY_KEYWORD_MAPPING = {
    "당뇨": "혈당",
    "고혈압": "혈압",
    "이상지질혈증": "콜레스테롤",
    "비만": "체지방 감소",
    "건강 기능 식품": "건강 기능 식품"
}


def search_by_main_fnctn(query_text, top_k=5):
    """
    주어진 쿼리 텍스트를 키워드 매핑 딕셔너리를 사용해 변환한 후, Pinecone에서 검색합니다.

    Args:
        query_text (str): 질병명.
        top_k (int): 검색 결과 개수.

    Returns:
        list: 검색 결과 리스트.
    """
    # 쿼리 텍스트를 매핑된 키워드로 변환
    if query_text in QUERY_KEYWORD_MAPPING:
        query_text = QUERY_KEYWORD_MAPPING[query_text]
    else:
        raise ValueError(f"'{query_text}'는 매핑된 키워드가 없습니다.")

    # 임베딩 생성 및 검색
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=OPENAI_API_KEY)
    query_vector = embeddings.embed_query(query_text)

    # Pinecone에서 검색
    search_results = index.query(vector=query_vector, top_k=top_k, include_metadata=True)
    results = [
        {
            "PRDUCT": result["metadata"]["PRDUCT"],
            "MAIN_FNCTN": result["metadata"]["MAIN_FNCTN"],
            "INTAKE_HINT1": result["metadata"].get("INTAKE_HINT1", "N/A"),
            "BASE_STANDARD": result["metadata"].get("BASE_STANDARD", "N/A"),
        }
        for result in search_results["matches"]
    ]
    return results


def search_by_prduct(product_name):
    query_filter = {"metadata.PRDUCT": {"$eq": product_name}}
    search_results = index.query(filter=query_filter, top_k=1, include_metadata=True)
    results = [
        {
            "PRDUCT": result["metadata"]["PRDUCT"],
            "MAIN_FNCTN": result["metadata"]["MAIN_FNCTN"],
            "INTAKE_HINT1": result["metadata"].get("INTAKE_HINT1", "N/A"),
            "BASE_STANDARD": result["metadata"].get("BASE_STANDARD", "N/A"),
        }
        for result in search_results["matches"]
    ]
    return results


def classify_risk(condition, probability):
    """
    위험도를 분류하고, 질병별로 적합한 메시지를 반환하는 함수.
    - 안전: 0 ~ 60
    - 의심: 61 ~ 80
    - 위험: 81 ~ 100
    """
    if probability <= 60:
        level = "안전"
        color = "success"
        if condition == "당뇨":
            message = "현재 혈당 상태는 안정적이고, 당뇨 위험도 낮은 편이에요! 그동안 건강한 생활 습관을 잘 지켜온 것 같아요, 지금 상태는 정말 좋아요."
        elif condition == "고혈압":
            message = "지금 혈압 상태는 정말 안정적이에요. 앞으로도 규칙적으로 혈압을 체크하면서 건강 상태를 점검하면, 좋은 상태를 오래 유지하실 수 있을 것 같아요."
        elif condition == "비만":
            message = "지금 체질량지수(BMI)와 건강 상태로 본 비만 위험이 낮은 상태예요, 지금처럼 건강한 식사와 운동을 꾸준히 실천하시면서, 활기차고 건강한 생활을 이어가봐요."
        elif condition == "이상지질혈증":
            message = "현재 혈중 지질 수치는 정상 범위에 있어요! 지금처럼 좋은 생활 습관을 유지하시면서 건강한 하루 되세요."
        else:
            message = "현재 건강 상태는 안전합니다. 꾸준히 관리하세요."
    elif 61 <= probability <= 80:
        level = "의심"
        color = "warning"
        if condition == "당뇨":
            message = "혈당이 조금 높아 당뇨로 이어질 가능성이 있으니 지금부터 주의가 필요해요. 당분 섭취를 줄이고 단백질이 풍부한 음식을 챙겨 드시면 큰 도움이 될 거예요. 또 가벼운 근력 운동을 시작해보세요."
        elif condition == "고혈압":
            message = "혈압이 조금 높아요. 음식을 짜게 드시지 않도록 신경 쓰고 운동도 큰 도움이 될 거예요. 꾸준히 실천하면 혈압이 안정되는 걸 느끼실 수 있을 거예요."
        elif condition == "비만":
            message = "현재 체질량지수(BMI)와 체지방률이 조금 높게 나왔어요. 가공식품과 고칼로리 음식을 줄이고, 신선한 채소, 통곡물, 단백질 중심으로 식사를 구성해보세요. 하루 30분 정도 빠르게 걷기겉운 유산소 운동으로 시작해보세요."
        elif condition == "이상지질혈증":
            message = "혈중 지질 수치가 살짝 높아요. 포화지방이나 트랜스지방이 많이 들어간 음식은 줄여봐요. 또 유산소 운동은 중성지방을 낮추고 좋은 콜레스테롤(HDL)을 높이는 데 큰 효과가 있어요."
        else:
            message = "건강 상태가 의심됩니다. 생활 습관을 점검하세요."
    else:
        level = "위험"
        color = "danger"
        if condition == "당뇨":
            message = "현재 혈당 상태는 당뇨 위험이 높은 단계로 보이네요. 지금이 중요한 시기인 만큼 관리가 꼭 필요해요. 우선 전문가와 상담을 받아 정밀 검진을 진행해봐요. 지금부터 시작하시면 건강을 되찾을 수 있어요."
        elif condition == "고혈압":
            message = "혈압 수치가 높아 심혈관 질환 같은 합병증 위험이 커질 수 있어요. 가공식품이나 인스턴트 음식은 꼭 피하시 게 좋아요. 무엇보다 전문가의 도움을 받는 게 가장 중요합니다. 병원을 방문하셔서 의사와 상담을 통해 필요한 약물 치료나 검사를 받아보세요."
        elif condition == "비만":
            message = "현재 비만 위험이 높은 단계에 속해 있어요. 이 상태에서는 당뇨, 고혈압, 심혈관 질환 같은 건강 문제로 이어질 수 있어요. 과도한 칼로리를 줄이고, 섬유질이 풍부한 식사를 하며 유산소 운동도 꾸준히 실천하시면 좋아요."
        elif condition == "이상지질혈증":
            message = "현재는 이상지질혈증 위험이 높은 상태라 적극적인 관리가 필요해 보여요. 심혈관 질환 같은 합병증 위험이 커질 수 있으니, 전문가와 함께 관리 방법을 찾아보시는 걸 추천드려요. 우선 식단 관리와 체력에 맞춰 근력 운동도 병행해볼까요?"
        else:
            message = "건강 상태가 좋지 않을 수 있습니다. 전문의 상담을 권장합니다."

    return level, message, color


def recommend_products(risk_levels):
    """
    위험 질병 개수에 따라 약을 추천하는 함수.
    - 4개 위험: 각 2개씩 (총 8개)
    - 3개 위험: 2, 3, 3개 (총 8개)
    - 2개 위험: 각 4개씩 (총 8개)
    - 1개 위험: 8개
    - 0개 위험: "건강 기능 식품"
    """
    # 위험인자의 개수 파악
    risks = [condition for condition, risk in risk_levels.items() if risk["level"] == "위험"]
    risk_count = len(risks)

    if risk_count == 4:
        return {condition: 2 for condition in risks}
    elif risk_count == 3:
        return {risks[0]: 2, risks[1]: 3, risks[2]: 3}
    elif risk_count == 2:
        return {condition: 4 for condition in risks}
    elif risk_count == 1:
        return {risks[0]: 8}
    else:
        return {"건강 기능 식품": 8}
    

def recommend_shop_products(risk_levels):
    """
    위험 질병 개수에 따라 약을 추천하는 함수.
    - 4개 위험: 각 2개, 3개 (총 9개)
    - 3개 위험: 3, 3, 3개 (총 9개)
    - 2개 위험: 5, 4개 (총 9개)
    - 1개 위험: 9개
    - 0개 위험: "건강 기능 식품" 9개
    """
    # 위험인자의 개수 파악
    risks = [condition for condition, risk in risk_levels.items() if risk["level"] == "위험"]
    risk_count = len(risks)

    if risk_count == 4:
        return {risks[0]: 2, risks[1]: 2, risks[2]: 3, risks[3]: 2}
    elif risk_count == 3:
        return {risks[0]: 3, risks[1]: 3, risks[2]: 3}
    elif risk_count == 2:
        return {risks[0]: 5, risks[1]: 4}
    elif risk_count == 1:
        return {risks[0]: 9}
    else:
        return {"건강 기능 식품": 9}
    

def calculate_overall_risk(probabilities):
    """
    질병 확률 값의 평균을 기반으로 위험 수준을 계산합니다.
    - 안전: 0 ~ 60
    - 의심: 61 ~ 80
    - 위험: 81 ~ 100
    """
    average_probability = sum(probabilities.values()) / len(probabilities)
    if average_probability <= 60:
        level = "안전"
        message = "현재 상태를 보니 대사증후군 위험이 낮은 편이에요! 그동안 건강한 생활 습관을 잘 유지해오신 덕분인 것 같아요."
    elif 61 <= average_probability <= 80:
        level = "의심"
        message = "지금 대사증후군 위험이 중간 수준으로 나타났어요. 혈압, 혈당, 콜레스테롤, 중성지방, 허리둘레 같은 여러 지표 중 일부가 정상 범위를 조금 벗어난 상태일 수 있어요."
    else:
        level = "위험"
        message = "현재 대사증후군 위험이 높은 상태로 평가되고있어요. 혈압, 혈당, 콜레스테롤, 중성지방, 허리둘레 등에서 이상 소견이 여러 개 나타나고 있는 상태 같아요. 심혈관 질환, 당뇨병 같은 합병증으로 이어질 수 있어 관리가 필요해요."

    return average_probability, level, message


# # 1. MAIN_FNCTN 유사도 검색
# # 혈압, 혈당, 콜레스테롤, 체지방
# query_text = "혈압 혈당 콜레스테롤 체지방"  # MAIN_FNCTN에 유사한 텍스트
# print("Searching for MAIN_FNCTN similarity...")
# similar_results = search_by_main_fnctn(index, query_text)
# print(json.dumps(similar_results, indent=4, ensure_ascii=False))