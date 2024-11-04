import os
import sys
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv(verbose=True)


CLINET_ID = os.getenv('CLINET_ID')
CLINET_SECRET = os.getenv("CLINET_SECRET")


def search_product(query):
    encText = urllib.parse.quote(query)
    url = "https://openapi.naver.com/v1/search/shop.json?query=" + encText # JSON 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", CLINET_ID)
    request.add_header("X-Naver-Client-Secret", CLINET_SECRET)
    response = urllib.request.urlopen(request)

    response_body = response.read()
    response_json = json.loads(response_body.decode('utf-8'))

    parsed_items = parse_products(response_json)
    
    return parsed_items


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
    
    return parsed_items[:6]