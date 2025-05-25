from typing import Dict
from collections import defaultdict
import json
from .embdr import embed_user_corpus
from .clsfr import classify_interests
from .otlg_loader import load_ontology_indexed_embeddings
from .io_util import load_user_dialogue_from_jsonl

def extract_user_interests(chat_jsonl_path, owl_path, top_n=5):
    """
    채팅로그, 온톨로지를 바탕으로 각 사용자별 top-N 관심 카테고리 추출.
    Returns: {user_id: [category, ...]}
    """
    user_corpus = load_user_dialogue_from_jsonl(chat_jsonl_path)
    user_ids, user_emb = embed_user_corpus(user_corpus)
    labels, label2cat, label_embs, _ = load_ontology_indexed_embeddings(owl_path)
    predictions = classify_interests(
        user_ids=user_ids,
        user_embeddings=user_emb,
        label_embeddings=label_embs,
        labels=labels,
        label2cat=label2cat,
        top_n=top_n
    )
    return predictions


def load_user_dialogue_from_jsonl(jsonl_path: str) -> Dict[str, str]:
    """
    .jsonl 채팅 로그에서 사용자별 전체 메시지를 병합하여 user_corpus 생성

    Args:
        jsonl_path (str): JSONL 파일 경로

    Returns:
        Dict[str, str]: {user_id: 전체 대화 문자열}
    """
    user_corpus = defaultdict(list)

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
                user = obj.get("sender")
                msg = obj.get("message")
                if user and msg:
                    user_corpus[user].append(msg)
            except json.JSONDecodeError:
                continue  # 잘못된 라인은 무시

    # 리스트를 하나의 문자열로 병합
    return {user: " ".join(msgs) for user, msgs in user_corpus.items()}
