# recommendation/model.py

from sentence_transformers import SentenceTransformer

# Load the pre-trained SBERT model
model = SentenceTransformer("all-MiniLM-L6-v2")
