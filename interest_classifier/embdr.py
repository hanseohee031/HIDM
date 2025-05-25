from typing import Tuple, List, Dict
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
def embed_user_corpus(
    user_corpus: Dict[str, str],
    model_name: str = "all-MiniLM-L6-v2"
) -> Tuple[List[str], np.ndarray]:
    """
    사용자별 대화문을 SBERT로 임베딩
    
    Args:
        user_corpus (Dict[str, str]): {user_id: 대화 문자열}
        model_name (str): SBERT 모델 이름
    
    Returns:
        Tuple[List[str], np.ndarray]: 사용자 ID 리스트, 임베딩 배열
    """
    model = SentenceTransformer(model_name)
    user_ids = list(user_corpus.keys())
    texts = list(user_corpus.values())
    embeddings = model.encode(texts, show_progress_bar=True)
    
    return user_ids, np.array(embeddings)
