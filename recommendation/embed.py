# embedding.py
import torch
from .model import model
from .preprocess import normalize_category

def get_user_embedding(category_list: list[str]) -> torch.Tensor:
    """
    사용자 관심사 카테고리 리스트를 SBERT로 평균 임베딩
    """
    if not category_list:
        raise ValueError("빈 관심사 리스트입니다.")

    normalized = [normalize_category(cat) for cat in category_list]
    embeddings = model.encode(normalized, convert_to_tensor=True)
    return embeddings.mean(dim=0)
