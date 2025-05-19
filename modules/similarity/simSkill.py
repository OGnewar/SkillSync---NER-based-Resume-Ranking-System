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
    jobFld = jobSkills.get("eduFields", []) + jobSkills.get("expFields", [])
    resFld = resSkills.get("eduFields", []) + resSkills.get("expFields", [])
    
    # print("SKILLS SIMILARITY")
    # print("---------------")
    # print(f"Job Hard Skills: {jobHar}")
    # print(f"Resume Hard Skills: {resHar}")
    # print(f"Job Soft Skills: {jobSof}")
    # print(f"Resume Soft Skills: {resSof}")
    # print(f"Job Tools: {jobToo}")
    # print(f"Resume Tools: {resToo}")
    # print(f"Job Products: {jobProd}")
    # print(f"Resume Products: {resProd}")
    # print(f"Job Fields: {jobFld}")
    # print(f"Resume Fields: {resFld}")
    
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
    
    # print(f"Hard Skill Score: {harScore}")
    # print(f"Soft Skill Score: {sofScore}")
    # print(f"Tools Score: {tooScore}")
    # print(f"Products Score: {proScore}")
    # print(f"Field Score: {fldScore}")
    
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
    
    # print("---------------")
    
    return round(score, 4)

