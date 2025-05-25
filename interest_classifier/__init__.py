from owlready2 import get_ontology
import tqdm
from pathlib import Path
from typing import List, Tuple, Dict
import numpy as np
import faiss
from collections import defaultdict
import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity