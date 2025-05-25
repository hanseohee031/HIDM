from typing import Tuple, List, Dict
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def classify_interests(
    user_ids: List[str],
    user_embeddings: np.ndarray,
    label_embeddings: np.ndarray,
    labels: List[str],
    label2cat: Dict[str, str],
    top_n: int = 5
) -> Dict[str, List[str]]:
    """
    사용자별로 top-N 유사 키워드를 기반으로 카테고리만 반환 (중복 제거)

    Returns:
        Dict[user_id, List[category]]
    """
    sim_matrix = cosine_similarity(user_embeddings, label_embeddings)
    result = {}

    for i, user in enumerate(user_ids):
        sim_scores = sim_matrix[i]
        top_indices = np.argsort(sim_scores)[::-1]

        seen_categories = set()
        top_categories = []

        for idx in top_indices:
            keyword = labels[idx]
            category = label2cat.get(keyword, "unknown")
            if category not in seen_categories:
                top_categories.append(category)
                seen_categories.add(category)
            if len(top_categories) >= top_n:
                break

        result[user] = top_categories

    return result
