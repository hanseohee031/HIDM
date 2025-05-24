# recommendation/preprocess.py

def normalize_category(cat_name: str) -> str:
    """
    온톨로지 기반 이름을 SBERT용 자연어로 변환.
    예: 'Self_Development_Career' → 'Self Development Career'
    """
    return cat_name.replace("_", " ").replace("-", " ").strip()


from typing import Dict, List

def preprocess_profiles(user_profiles: Dict[str, List[str]]) -> Dict[str, str]:
    """
    각 유저의 카테고리 리스트를 normalize_category로 정규화한 뒤,
    하나의 문장(String)으로 합쳐 SBERT 입력용 텍스트로 변환합니다.
    """
    processed: Dict[str, str] = {}
    for user_id, categories in user_profiles.items():
        normalized = [normalize_category(cat) for cat in categories]
        # 띄어쓰기로 연결
        processed[user_id] = " ".join(normalized)
    return processed
