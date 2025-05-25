from typing import Tuple, List, Dict
from pathlib import Path
import numpy as np
import faiss
from owlready2 import get_ontology
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity





def load_ontology_indexed_embeddings(
    owl_path: str, model_name: str = "all-MiniLM-L6-v2"
) -> Tuple[List[str], Dict[str, str], np.ndarray, faiss.IndexFlatIP]:
    """
    온톨로지 인스턴스를 로딩하고 키워드, 카테고리 매핑, 임베딩, FAISS 인덱스를 반환한다.
    
    Args:
        owl_path (str): OWL 파일 경로
        model_name (str): SBERT 모델 이름
    
    Returns:
        labels (List[str]): 인스턴스 키워드 라벨
        label2cat (Dict[str, str]): 키워드 → 카테고리 매핑
        lab_vecs (np.ndarray): SBERT 임베딩 벡터
        faiss_index (faiss.IndexFlatIP): 벡터 검색용 인덱스
    """
    owl_file = Path(owl_path)
    if not owl_file.exists():
        raise FileNotFoundError(f"OWL file not found: {owl_path}")

    onto = get_ontology(str(owl_file.resolve())).load(reload=True)
    print("Individual 개수:", len(list(onto.individuals())))

    sbert = SentenceTransformer(model_name)
    labels = []
    embeddings = []
    label2cat = {}

    for ind in onto.individuals():
        kw = ind.label[0] if ind.label else ind.name
        for cls in ind.is_a:
            cat = cls.label[0] if cls.label else cls.name
            labels.append(kw)
            label2cat[kw] = cat
            embeddings.append(sbert.encode(kw))

    lab_vecs = np.array(embeddings)
    if lab_vecs.ndim == 1:
        lab_vecs = lab_vecs[None, :]

    index = faiss.IndexFlatIP(lab_vecs.shape[1])
    index.add(lab_vecs)

    print("FAISS 라벨 수:", index.ntotal)
    return labels, label2cat, lab_vecs, index
