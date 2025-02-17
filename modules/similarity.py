'''from sentence_transformers import SentenceTransformer, util
#sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
sbert_model = SentenceTransformer('nli-roberta-base-v2') #fine-tuned sentiment-aware embeddings

def calculate_similarity(job_features, resume_features):

    job_embedding = sbert_model.encode(str(job_features), convert_to_tensor=True)
    resume_embedding = sbert_model.encode(str(resume_features), convert_to_tensor=True)

    similarity_score = util.cos_sim(job_embedding, resume_embedding).item()
    return similarity_score'''
    
from sentence_transformers import SentenceTransformer, util
import re

def normalize_text(text):
    return re.sub(r'[^a-zA-Z0-9 ]', '', text.lower().strip())

def calculate_feature_similarity(model, feature_1, feature_2):
    """
    Compute similarity for individual features using SBERT.
    """
    text1, text2 = normalize_text(feature_1), normalize_text(feature_2)
    embedding1 = model.encode(text1, convert_to_tensor=True)
    embedding2 = model.encode(text2, convert_to_tensor=True)
    return util.pytorch_cos_sim(embedding1, embedding2).item()

def calculate_similarity(resume, job):
    """
    Compute weighted similarity score based on individual feature similarities.
    """
    weights = {
    'experience': 0.20,
    'education': 0.15,
    'certification': 0.10,
    'hard': 0.20,
    'soft': 0.10,
    'tools': 0.20,
    'sector': 0.05
    }
    model = SentenceTransformer('nli-roberta-base-v2')
    
    feature_similarities = {
        'experience': calculate_feature_similarity(model, resume.get('experience', ''), job.get('experience', '')),
        'education': calculate_feature_similarity(model, resume.get('education', ''), job.get('education', '')),
        'certification': calculate_feature_similarity(model, resume.get('certification', ''), job.get('certification', '')),
        'hard': calculate_feature_similarity(model, resume.get('hard', ''), job.get('hard', '')),
        'soft': calculate_feature_similarity(model, resume.get('soft', ''), job.get('soft', '')),
        'tools': calculate_feature_similarity(model, resume.get('tools', ''), job.get('tools', '')),
        'sector': calculate_feature_similarity(model, resume.get('sector', ''), job.get('sector', ''))
    }
    
    total_similarity = sum(feature_similarities[key] * weights.get(key, 0) for key in feature_similarities)
    
    return total_similarity

