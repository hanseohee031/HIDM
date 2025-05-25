[ 관심사 분류 파이프라인 ]

사용자 채팅 로그(.jsonl) + 온톨로지(.owl)를 기반으로
SBERT 임베딩 → 키워드 유사도 계산 → 카테고리 분류를 수행합니다.


[ 실행 흐름 요약 ]

1. 채팅 로그 로딩 → 사용자별 발화 병합
2. 사용자 문장 SBERT 임베딩
3. 온톨로지 인스턴스 로딩 → 키워드 임베딩
4. 사용자 ↔ 키워드 유사도 계산
5. Top-N 카테고리 분류
6. JSON 저장 (또는 기존 사용자 목록 병합)


[ 주요 함수 및 매개변수 설명 ]

1. load_ontology_indexed_embeddings(owl_path, model_name="...")
  - owl_path: 온톨로지 OWL 파일 경로
  - model_name: SBERT 모델 이름
  → 라벨 리스트, 카테고리 매핑, 임베딩, FAISS 인덱스 반환

2. load_user_dialogue_from_jsonl(jsonl_path)
  - jsonl_path: 채팅 로그(.jsonl) 경로
  → user_corpus: {user_id: 전체 발화 문자열}

3. embed_user_corpus(user_corpus, model_name="...")
  - user_corpus: 사용자별 병합된 문장 딕셔너리
  - model_name: SBERT 모델 이름
  → 사용자 ID 리스트, 임베딩 배열 반환

4. classify_interests(user_ids, user_embeddings, label_embeddings, labels, label2cat, top_n)
  - user_ids: 사용자 ID 리스트
  - user_embeddings: 사용자 발화 임베딩
  - label_embeddings: 온톨로지 키워드 임베딩
  - labels: 키워드 리스트
  - label2cat: 키워드 → 카테고리 매핑
  - top_n: 최대 카테고리 수
  → {user_id: [category1, category2, ...]} 반환

5. save_profiles_to_json(profiles, path)
  - profiles: 분류 결과 딕셔너리
  - path: 저장 경로

6. update_user_profiles(user_list_path, profiles_path, output_path)
  - user_list_path: 전체 사용자 JSON
  - profiles_path: 관심사 결과 JSON
  - output_path: 병합 결과 저장 경로


[ main 예시 (파이썬 기준) ]

def test_main():
    # 테스트용 파일 경로
    chat_jsonl_path = "fake_chat.jsonl"
    owl_path = "interest.owl"
    output_path = "test_profiles.json"
    top_n = 5

    print("[1] 채팅 로그 로딩 중...")
    user_corpus = load_user_dialogue_from_jsonl(chat_jsonl_path)

    print("[2] 사용자 임베딩 수행 중...")
    user_ids, user_emb = embed_user_corpus(user_corpus)

    print("[3] 온톨로지 로딩 및 키워드 임베딩 중...")
    labels, label2cat, label_embs, _ = load_ontology_indexed_embeddings(owl_path)

    print("[4] 관심사 분류 중...")
    predictions = classify_interests(
        user_ids=user_ids,
        user_embeddings=user_emb,
        label_embeddings=label_embs,
        labels=labels,
        label2cat=label2cat,
        top_n=top_n
    )
    
    print(f"[5] 결과 저장 중: {output_path}")
    save_profiles_to_json(predictions, output_path)

    print("[✔] 테스트 완료. 파일을 확인하세요.")


if __name__ == "__main__":
    test_main()

---------------------------------------------------
[1] 채팅 로그 로딩 중...
[2] 사용자 임베딩 수행 중...
Batches: 100%|██████████| 1/1 [00:00<00:00, 37.36it/s]
[3] 온톨로지 로딩 및 키워드 임베딩 중...
Individual 개수: 272
FAISS 라벨 수: 272
[4] 관심사 분류 중...
[5] 결과 저장 중: test_profiles.json
[✔] 테스트 완료. 파일을 확인하세요.