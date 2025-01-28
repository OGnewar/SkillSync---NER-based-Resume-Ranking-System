from sentence_transformers import SentenceTransformer, util
sbert_model = SentenceTransformer('all-MiniLM-L6-v2')


def calculate_similarity(job_features, resume_features):

    job_embedding = sbert_model.encode(str(job_features), convert_to_tensor=True)
    resume_embedding = sbert_model.encode(str(resume_features), convert_to_tensor=True)

    similarity_score = util.cos_sim(job_embedding, resume_embedding).item()
    return similarity_score