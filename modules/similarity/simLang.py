
'''from sentence_transformers import SentenceTransformer, util

# Load the SBERT model
model = SentenceTransformer('nli-roberta-base-v2')

def cosine_similarity(text1, text2):
    """Compute cosine similarity between two texts using SBERT."""
    if not text1 or not text2:
        return 0.0
    embeddings = model.encode([text1, text2], convert_to_tensor=True)
    return util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()

def language_similarity(job_features, resume_features):
    # Extract languages and proficiency, handling missing fields
    job_languages = [
        " ".join(filter(None, pair)) for pair in zip(
            job_features.get("language", {}).get("lang", []),
            job_features.get("language", {}).get("langProf", [])
        )
    ]
    
    resume_languages = [
        " ".join(filter(None, pair)) for pair in zip(
            resume_features.get("language", {}).get("lang", []),
            resume_features.get("language", {}).get("langProf", [])
        )
    ]
    
    print(f"Job Language: {job_languages}")
    print(f"Resume Language: {resume_languages}")

    # Compute similarity between job and resume languages
    if not job_languages or not resume_languages:
        return 0.0  # If either side is missing, return 0 similarity

    lang_scores = [
        max(cosine_similarity(job_lang, resume_lang) for resume_lang in resume_languages)
        for job_lang in job_languages
    ] if job_languages and resume_languages else [0.0]

    max_lang_score = sum(lang_scores) / len(lang_scores) if lang_scores else 0.0

    return round(max_lang_score, 4)'''
    
from sentence_transformers import SentenceTransformer, util

# Load the SBERT model
model = SentenceTransformer('nli-roberta-base-v2')

def cosine_similarity(text1, text2):
    if not text1 or not text2:
        return 0
    embeddings = model.encode([text1, text2], convert_to_tensor=True)
    return util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()

def language_similarity(job, res):
    jobLangs = job.get("language", {})
    resLangs = res.get("language", {})
    
    jobLang = jobLangs.get("langs", [])
    resLang = resLangs.get("langs", [])
    jobProf = jobLangs.get("langProfs", [])
    resProf = resLangs.get("langProfs", [])
    
    print("LANGUAGE SIMILARITY")
    print("------------")
    print(f"Job Languages: {jobLang}")
    print(f"Resume Language: {resLang}")
    print(f"Job Proficiency: {jobProf}")
    print(f"resume Proficiency: {resProf}")
    
    jobLangStr = ", ".join(jobLang)
    resLangStr = ", ".join(resLang)
    
    langScore = cosine_similarity(jobLangStr, resLangStr)
    
    print(f"Language Score: {langScore}")
    
    prof = {
        "Basic": 1, "basic": 1, "Basics": 1, "baiscs": 1, "intermediate": 2, "Intermediate": 2, "Intermed": 2, "Conversational": 2.5, "fluent": 3, "fluency": 3, "Fluent": 3, "advanced": 4, "Advanced": 4
    }
    
    jobLangProf = [prof.get(pro, -1) for pro in jobProf]
    resLangProf = [prof.get(pro, -1) for pro in resProf]
    
    print(f"Job Proficiency: {jobLangProf}")
    print(f"Resume Proficiency: {resLangProf}")
    
    if not jobLangProf or not resLangProf:
        return 0.0
    
    minJobProf = min(jobLangProf)
    maxResProf = max(resLangProf)
    
    if maxResProf >= minJobProf:
        proScore = 1.0
    else:
        diff = minJobProf - maxResProf
        proScore = max(0, 1.0 - (diff / 3))  # Normalize difference with max priority 3

    print(f"Proficiency Score: {proScore}")
    
    weights = {
        "lang": 0.5,
        "prof": 0.5
    }
    
    if not jobProf:
        weights["lang"] += 0.3
        weights["prof"] = 0.0
    
    score = 0.5 * langScore + 0.5 * proScore
    
    print("---------------")
    
    return round(score, 4)


