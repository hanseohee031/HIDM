# recommendation/recommend.py

import torch
from torch.nn.functional import cosine_similarity

from .embed import get_user_embedding
from .preprocess import preprocess_profiles  # 필요 시 사용 가능
from accounts.models import UserProfile


def recommend_similar_users(
    user_id: str,
    user_profiles: dict[str, list[str]],
    top_k: int = 3
) -> list[dict]:
    """
    지정된 user_id에 대해 SBERT 임베딩 기반 cosine similarity로
    추천 사용자 목록을 반환합니다. 같은 성별 사용자에게는
    (1 − raw_score)의 2% 만큼 추가 가중치를 부여합니다.
    """
    # user_profiles에 대상이 없으면 에러
    if user_id not in user_profiles:
        raise ValueError(f"{user_id} is not in user_profiles.")

    # 1) 모든 사용자에 대해 임베딩 생성
    user_embs: dict[str, torch.Tensor] = {
        uid: get_user_embedding(cats)
        for uid, cats in user_profiles.items()
    }

    # 2) 대상 사용자 임베딩 & 성별 조회
    target_emb = user_embs[user_id]
    me_gender = UserProfile.objects.get(user__username=user_id).gender

    # 3) 코사인 유사도 계산 및 성별 가중치 반영
    similarities: dict[str, float] = {}
    for uid, emb in user_embs.items():
        if uid == user_id:
            continue

        # 기본 cosine similarity
        raw_score = cosine_similarity(
            target_emb.unsqueeze(0),
            emb.unsqueeze(0)
        ).item()

        score = raw_score
        # 같은 성별이면 남은 여유(1−raw_score)의 2%만큼 추가
        if UserProfile.objects.filter(user__username=uid).exists():
            other_gender = UserProfile.objects.get(user__username=uid).gender
            if other_gender == me_gender:
                weight = 0.02
                score = score + weight * (1.0 - score)

        similarities[uid] = score

    # 4) 유사도 순으로 정렬하여 상위 top_k 추출
    top_users = sorted(
        similarities.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_k]

    # 5) 결과 포맷 맞춰 반환
    return [
        {"user": uid, "score": round(score, 4)}
        for uid, score in top_users
    ]
