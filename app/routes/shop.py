import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv(verbose=True)

CLINET_ID = os.getenv('CLINET_ID')
CLINET_SECRET = os.getenv("CLINET_SECRET")

disease_mapping = {
        "당뇨": "혈당 조절 식품",
        "고혈압": "혈압 조절 식품",
        "비만": "체지방 감소 식품",
        "이상지질혈증": "콜레스테롤 감소 식품",
        "건강 기능 식품": "비타민"
    }

def search_product(recommended_counts):
    """
    질병별로 Naver 쇼핑 API에 요청하여 추천 제품을 검색합니다.
    
    Parameters:
        recommended_counts (dict): {"질병명": top_k값} 형태의 추천 개수
    
    Returns:
        list: 모든 검색된 추천 제품 리스트
    """
    all_items = []  # 모든 제품을 저장할 리스트

    for disease, top_k in recommended_counts.items():
        mapped_query = disease_mapping.get(disease, disease)
        encText = urllib.parse.quote(mapped_query)
        url = f"https://openapi.naver.com/v1/search/shop.json?query={encText}&display={top_k}"  # top_k에 따라 표시 개수 결정
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", CLINET_ID)
        request.add_header("X-Naver-Client-Secret", CLINET_SECRET)
        
        try:
            response = urllib.request.urlopen(request)
            response_body = response.read()
            response_json = json.loads(response_body.decode('utf-8'))

            # 제품 파싱 및 저장
            parsed_items = parse_products(response_json)
            all_items.extend(parsed_items)  # 기존 리스트에 추가
        
        except Exception as e:
            print(f"Error fetching data for {disease}: {e}")
    
    return all_items


def parse_products(data):
    """
    주어진 데이터에서 원하는 필드들을 추출하여 리스트로 반환합니다.
    
    Args:
        data (dict): 파싱할 데이터 딕셔너리
    
    Returns:
        list of dict: 추출된 필드들로 구성된 리스트
    """
    parsed_items = []
    
    if 'items' in data and isinstance(data['items'], list):
        for item in data['items']:
            
            # 각 아이템에서 필요한 필드 추출
            parsed_item = {
                'title': item.get('title', '').replace('<b>', '').replace('</b>', ''),  # HTML 태그 제거
                'link': item.get('link', ''),
                'image': item.get('image', ''),
                'lprice': item.get('lprice', '0'),
                'mallName': item.get('mallName', '')
            }
            parsed_items.append(parsed_item)
    else:
        print("No items found in data.")
    
    return parsed_items