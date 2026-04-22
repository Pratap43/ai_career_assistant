from sentence_transformers import SentenceTransformer, util
import re

# Load model (only once)
model = SentenceTransformer('all-MiniLM-L6-v2')


# Clean text
def preprocess(text):
    text = text.lower()
    text = text.replace("ml", "machine learning")
    return text


# 🔥 AI-based similarity
def calculate_score(resume, jd):
    resume = preprocess(resume)
    jd = preprocess(jd)

    # Convert to embeddings
    emb1 = model.encode(resume, convert_to_tensor=True)
    emb2 = model.encode(jd, convert_to_tensor=True)

    # Cosine similarity (semantic)
    score = util.cos_sim(emb1, emb2).item() * 100

    return round(score, 2)


# Better tokenization
def tokenize(text):
    return set(re.findall(r'\b\w+\b', text.lower()))


def missing_skills(resume, jd):
    resume_words = tokenize(resume)
    jd_words = tokenize(jd)

    return list(jd_words - resume_words)[:10]


def recommend_jobs(resume):
    r = resume.lower()
    roles = []

    if "machine learning" in r:
        roles.append("ML Engineer")
    if "data" in r:
        roles.append("Data Analyst")
    if "web" in r:
        roles.append("Frontend Developer")

    return roles if roles else ["Software Developer"]