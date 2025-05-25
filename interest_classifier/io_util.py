from typing import List, Dict
import json

def save_profiles_to_json(
    profiles: Dict[str, List[Dict[str, float]]],
    output_path: str
) -> None:
    """
    사용자 관심사 분류 결과를 JSON 파일로 저장 (점수 포함)

    Args:
        profiles: {user_id: [{"keyword": str, "score": float}, ...]}
        output_path: 저장할 JSON 파일 경로
    """
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=2)


def update_user_profiles(
    user_list_path: str,
    profiles_path: str,
    output_path: str
) -> None:
    """
    기존 사용자 목록(user_list_path)에 관심사 분류 결과(profiles_path)를 업데이트하여 저장

    Args:
        user_list_path: 전체 사용자 정보 JSON (리스트)
        profiles_path: 분류된 관심사 결과 JSON (user_id → 관심사 리스트)
        output_path: 병합 결과 저장 경로
    """
    with open(user_list_path, "r", encoding="utf-8") as f:
        users = json.load(f)

    with open(profiles_path, "r", encoding="utf-8") as f:
        profiles = json.load(f)

    for user in users:
        uid = user.get("user_id")
        if uid in profiles:
            user["interests"] = profiles[uid]  # 최신 결과로 덮어쓰기

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


from typing import Dict
from collections import defaultdict
import json

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
