# run_pipeline.py

from dialog_prcr import load_user_dialogue_from_jsonl
from embdr import embed_user_corpus
from otlg_loader import load_ontology_indexed_embeddings
from clsfr import classify_interests
from io_util import save_profiles_to_json

def main():
    # (1) 채팅 로그 로딩
    chat_jsonl = "fake_chat.jsonl"
    user_corpus = load_user_dialogue_from_jsonl(chat_jsonl)

    # (2) 사용자 임베딩
    user_ids, user_embs = embed_user_corpus(user_corpus)

    # (3) 온톨로지 로딩 및 키워드 임베딩
    owl_file = "interest.owl"
    labels, label2cat, label_embs, _ = load_ontology_indexed_embeddings(owl_file)

    # (4) 관심사 분류
    top_n = 5
    results = classify_interests(
        user_ids=user_ids,
        user_embeddings=user_embs,
        label_embeddings=label_embs,
        labels=labels,
        label2cat=label2cat,
        top_n=top_n
    )

    # (5) JSON으로 저장
    out_path = "profiles.json"
    save_profiles_to_json(results, out_path)
    print(f"✅ 완료! 결과가 `{out_path}` 에 저장되었습니다.")

if __name__ == "__main__":
    main()
