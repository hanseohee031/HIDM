# recommendation/test_recommend.py

from recommendation.recommend import recommend_similar_users

# 예시: 가상의 유저 → 관심사 매핑
user_profiles = {
    'alice': ['Travel', 'Music', 'Food'],
    'bob':   ['Sports', 'Travel', 'Social'],
    'carol': ['Music', 'Art', 'Culture'],
    'dave':  ['Food', 'Tech', 'Gaming'],
}

# alice 에게 2명 추천
results = recommend_similar_users('alice', user_profiles, top_k=2)
print(results)
# 예상 출력 예: [{'user':'dave','score':0.82}, {'user':'bob','score':0.74}]
