# recommendation/recommend.py

import torch
from torch.nn.functional import cosine_similarity

from .embed import get_user_embedding
from .preprocess import preprocess_profiles  # 이제 정상 import 됩니다.

def recommend_similar_users(user_id: str,
                            user_profiles: dict[str, list[str]],
                            top_k: int = 3) -> list[dict]:
    """
    지정된 user_id에 대해 cosine similarity 기반 추천 사용자 목록을 반환합니다.
    """
    if user_id not in user_profiles:
        raise ValueError(f"{user_id} is not in user_profiles.")

    # (선택) 전체 프로필을 텍스트로 전처리하고 싶다면 아래처럼 사용할 수 있습니다.
    # text_profiles = preprocess_profiles(user_profiles)

    # 기존 방식: 각 카테고리 리스트를 바로 임베딩
    user_embs = {
        uid: get_user_embedding(cats)
        for uid, cats in user_profiles.items()
    }
    target_emb = user_embs[user_id]

    similarities = {
        uid: cosine_similarity(
                target_emb.unsqueeze(0),
                emb.unsqueeze(0)
            ).item()
        for uid, emb in user_embs.items()
        if uid != user_id
    }

    top_users = sorted(
        similarities.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_k]

    return [
        {"user": uid, "score": round(score, 4)}
        for uid, score in top_users
    ]
