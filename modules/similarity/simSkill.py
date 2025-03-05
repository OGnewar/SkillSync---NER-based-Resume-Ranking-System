
'''from sentence_transformers import SentenceTransformer, util

# Load the SBERT model
model = SentenceTransformer('nli-roberta-base-v2')

def cosine_similarity(text1, text2):
    """Compute cosine similarity between two texts using SBERT."""
    if not text1 or not text2:
        return 0
    embeddings = model.encode([text1, text2], convert_to_tensor=True)
    return util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()

def skill_similarity(job_features, resume_features):
    # Extract skills with default empty lists if missing
    job_skills = job_features.get("skills", {})
    resume_skills = resume_features.get("skills", {})

    job_hard_skills = job_skills.get("hard", [])
    job_tools = job_skills.get("tools", [])
    job_products = job_skills.get("products", [])
    resume_hard_skills = resume_skills.get("hard", [])
    resume_tools = resume_skills.get("tools", [])
    resume_products = resume_skills.get("products", [])

    job_soft_skills = job_skills.get("soft", [])
    resume_soft_skills = resume_skills.get("soft", [])

    # Combine all technical skills
    job_technical_skills = job_hard_skills + job_tools + job_products
    resume_technical_skills = resume_hard_skills + resume_tools + resume_products
    
    print(f"Job Technical Skills: {job_technical_skills}")
    print(f"Resume Technical Skills: {resume_technical_skills}")
    print(f"Job Soft Skills: {job_soft_skills}")
    print(f"Resume Soft Skills: {resume_soft_skills}")

    # Compute similarity for technical skills
    tech_scores = [
        max(cosine_similarity(job_skill, resume_skill) for resume_skill in resume_technical_skills)
        for job_skill in job_technical_skills
    ] if job_technical_skills and resume_technical_skills else [0]

    max_tech_score = sum(tech_scores) / len(tech_scores) if tech_scores else 0

    # Compute similarity for soft skills
    soft_scores = [
        max(cosine_similarity(job_skill, resume_skill) for resume_skill in resume_soft_skills)
        for job_skill in job_soft_skills
    ] if job_soft_skills and resume_soft_skills else [0]

    max_soft_score = sum(soft_scores) / len(soft_scores) if soft_scores else 0

    # **Dynamic Weighting Based on Missing Technical Skills**
    base_tech_weight, base_soft_weight = 0.8, 0.2

    # Increase technical weight if any tech category is missing
    missing_hard = not bool(job_hard_skills)
    missing_tools = not bool(job_tools)
    missing_products = not bool(job_products)

    # Redistribute the missing weights
    if missing_hard:
        base_soft_weight += 0.1
    if missing_tools:
        base_soft_weight += 0.1
    if missing_products:
        base_soft_weight += 0.05

    # Ensure weights sum to 1
    total_weight = base_tech_weight + base_soft_weight
    tech_weight = base_tech_weight / total_weight
    soft_weight = base_soft_weight / total_weight

    # Compute final similarity score
    final_score = (tech_weight * max_tech_score) + (soft_weight * max_soft_score)

    # Ensure the max score remains 1.0
    return round(min(final_score, 1.0), 4)'''
    
from sentence_transformers import SentenceTransformer, util

# Load the SBERT model
model = SentenceTransformer('nli-roberta-base-v2')

def cosine_similarity(text1, text2):
    if not text1 or not text2:
        return 0
    embeddings = model.encode([text1, text2], convert_to_tensor=True)
    return util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()

def skill_similarity(job, res):
    jobSkills = job.get("skills", {})
    resSkills = res.get("skills", {})
    
    jobHar = jobSkills.get("hards", [])
    resHar = resSkills.get("hards", [])
    jobSof = jobSkills.get("softs", [])
    resSof = resSkills.get("softs", [])
    jobToo = jobSkills.get("tools", [])
    resToo = resSkills.get("tools", [])
    jobProd = jobSkills.get("products", [])
    resProd = resSkills.get("products", [])
    jobFld = jobSkills.get("eduFields", []) + resSkills.get("expFields", [])
    resFld = resSkills.get("eduFields", [])
    
    print("SKILLS SIMILARITY")
    print("---------------")
    print(f"Job Hard Skills: {jobHar}")
    print(f"Resume Hard Skills: {resHar}")
    print(f"Job Soft Skills: {jobSof}")
    print(f"Resume Soft Skills: {resSof}")
    print(f"Job Tools: {jobToo}")
    print(f"Resume Tools: {resToo}")
    print(f"Job Products: {jobProd}")
    print(f"Resume Products: {resProd}")
    print(f"Job Fields: {jobFld}")
    print(f"Resume Fields: {resFld}")
    
    jobHarStr = ", ".join(jobHar)
    resHarStr = ", ".join(resHar)
    jobSofStr = ", ".join(jobSof)
    resSofStr = ", ".join(resSof)
    jobTooStr = ", ".join(jobToo)
    resTooStr = ", ".join(resToo)
    jobProStr = ", ".join(jobProd)
    resProStr = ", ".join(resProd)
    jobFldStr = ", ".join(jobFld)
    resFldStr = ", ".join(resFld)
    
    harScore = cosine_similarity(jobHarStr, resHarStr)
    sofScore = cosine_similarity(jobSofStr, resSofStr)
    tooScore = cosine_similarity(jobTooStr, resTooStr)
    proScore = cosine_similarity(jobProStr, resProStr)
    fldScore = cosine_similarity(jobFldStr, resFldStr)
    
    print(f"Hard Skill Score: {harScore}")
    print(f"Soft Skill Score: {sofScore}")
    print(f"Tools Score: {tooScore}")
    print(f"Products Score: {proScore}")
    print(f"Field Score: {fldScore}")
    
    weights = {
        "hard": 0.25,
        "tools": 0.25,
        "products": 0.2,
        "soft": 0.15,
        "field": 0.15
    }
    
    if not jobProd:
        weights["hard"] += 0.1
        weights["tools"] += 0.1
        weights["products"] = 0.0
        
    if not jobSof:
        weights["hard"] += 0.05
        weights["tools"] += 0.05
        weights["field"] += 0.05
        weights["soft"] =0
        
    if not jobFld:
        weights["hard"] += 0.05
        weights["tools"] += 0.05
        if jobProd:
            weights["products"] += 0.05
        else:
            weights["hard"] += 0.025
            weights["tools"] += 0.025
        weights["field"] =0
        
    score = weights["hard"] * harScore + weights["tools"] * tooScore + weights["products"] * proScore + weights["soft"] * sofScore + weights["field"] * fldScore
    
    print("---------------")
    
    return round(score, 4)

