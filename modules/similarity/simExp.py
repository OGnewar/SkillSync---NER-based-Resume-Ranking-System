import re
from dateparser import parse
from datetime import datetime
from sentence_transformers import SentenceTransformer, util
from modules.features.exMnths import extract_months

# Load SBERT model
model = SentenceTransformer("nli-roberta-base-v2")

def cosine_similarity(text1, text2):
    if not text1 or not text2:
        return 0.0
    embeddings = model.encode([text1, text2], convert_to_tensor=True)
    return util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()

def experience_similarity(job, res):
    # Get job and resume details
    jobDetails = job.get("experience", {})
    resDetails = res.get("experience", {})
    
    # Extract job and resume features
    jobTitles = jobDetails.get("title", [])
    resRoles = resDetails.get("expRoles", [])
    jobRoles = jobDetails.get("expRoles", [])
    jobFields = jobDetails.get("expFields", []) + jobDetails.get("eduFields", [])
    resFields = resDetails.get("eduFields", [])
    jobYrs = jobDetails.get("expYrs", [])
    resYrs = resDetails.get("expYrs", [])
    jobMonths = jobDetails.get("expMonths", [])
    resMonths = resDetails.get("expMonths", [])
    jobMnths = jobDetails.get("expMnths", 0.0)
    resMnths = resDetails.get("expMnths", 0.0)
    jobHardSkills = jobDetails.get("hards", [])
    resHardSkills = resDetails.get("hards", [])
    jobTools = jobDetails.get("tools", [])
    resTools = resDetails.get("tools", [])
    jobProds = jobDetails.get("products", [])
    resProds = resDetails.get("products", [])
    jobSectors = jobDetails.get("sectors", [])
    resSectors = resDetails.get("sectors", [])
    
    print("EXPERIENCE SIMILARITY")
    print("------------------")
    print(f"Job Titles: {jobTitles}")
    print(f"Resume Roles: {resRoles}")
    print(f"Job Roles: {jobRoles}")
    print(f"Job Fields: {jobFields}")
    print(f"Resume Fields: {resFields}")
    print(f"Job Years: {jobYrs}")
    print(f"Job Months: {jobMonths}")
    print(f"Job Total Months: {jobMnths}")
    print(f"Resume Years: {resYrs}")
    print(f"Resume Months: {resMonths}")
    print(f"Resume Total Months: {resMnths}")
    #print(f"Job Hard Skills: {jobHardSkills}")
    #print(f"Resume Hard Skills: {resHardSkills}")
    #print(f"Job Tools: {jobTools}")
    #print(f"Job Resume Tools: {resTools}")
    #print(f"Job Products: {jobProds}")
    #print(f"Resume Products: {resProds}")
    print(f"Job Sectors: {jobSectors}")
    print(f"Resume Sectors: {resSectors}")
    
    # Convert features to strings
    jobTitStr = ", ".join(jobTitles)
    resRolStr = ", ".join(resRoles)
    jobRolStr = ", ".join(jobRoles)
    jobFidStr = ", ".join(jobFields)
    resFidStr = ", ".join(resFields)
    jobHadStr = ", ".join(jobHardSkills)
    resHadStr = ", ".join(resHardSkills)
    jobTooStr = ", ".join(jobTools)
    resTooStr = ", ".join(resTools)
    jobProStr = ", ".join(jobProds)
    resProStr = ", ".join(resProds)
    jobSecStr = ", ".join(jobSectors)
    resSecStr = ", ".join(resSectors)

    # Compare Job titles with resume roles
    titleScore = cosine_similarity(jobTitStr, resRolStr)
    rolScore = cosine_similarity(jobRolStr, resTooStr)
    fldScore = cosine_similarity(jobFidStr, resFidStr)
    hadScore = cosine_similarity(jobHadStr, resHadStr)
    tooScore = cosine_similarity(jobTooStr, resTooStr)
    prodScore = cosine_similarity(jobProStr, resProStr)
    secScore = cosine_similarity(jobSecStr, resSecStr)
    
    print(f"Title Score: {titleScore}")
    print(f"Role Score: {rolScore}")
    print(f"Field Score: {fldScore}")
    print(f"Hard Skill Score: {hadScore}")
    print(f"Tools Score: {tooScore}")
    print(f"Products Score: {prodScore}")
    print(f"Sector Score: {secScore}")
    
    # Assign Weights
    preScoreWeights = {
        "title": 0.3,
        "role": 0.1,
        "field": 0.1,
        "hard": 0.15,
        "tools": 0.15,
        "products": 0.15,
        "sectors": 0.05
    }
    
    if not jobRoles:
        preScoreWeights["title"] += 0.1
        preScoreWeights["role"] = 0.0
        
    if not jobFields:
        preScoreWeights["title"] += 0.05
        preScoreWeights["hard"] += 0.05
        preScoreWeights["field"] = 0.0
        
    if not jobProds:
        preScoreWeights["title"] += 0.05
        preScoreWeights["hard"] += 0.05
        preScoreWeights["tools"] += 0.05
        preScoreWeights["products"] = 0.0
        
    if not jobSectors:
        preScoreWeights["title"] += 0.05
        preScoreWeights["sectors"] = 0.0
        
    preScore = preScoreWeights["title"] * titleScore + preScoreWeights["role"] * rolScore + preScoreWeights["field"] * fldScore + preScoreWeights["hard"] * hadScore + preScoreWeights["tools"] * tooScore + preScoreWeights["products"] * prodScore + preScoreWeights["sectors"] * secScore
    
    print(f"Pre Score: {preScore}")
    
    factor = preScore ** 2
    print(f"Factor: {factor}")
    
    durationScore = 0.0
    
    if preScore > 0.5 and jobMnths and resMnths:
        if resMnths >= jobMnths:
            durationScore = 1.0
        else:
            durationScore = 1 - abs(jobMnths - resMnths) / max(jobMnths, resMnths) if max(jobMnths, resMnths) > 0 else 0
    else:
        if resMnths >= jobMnths:
            durationScore = 1.0
        else:
            durationScore = 1 - abs(jobMnths - resMnths) / max(jobMnths, resMnths) if max(jobMnths, resMnths) > 0 else 0
            durationScore /= 2
        
    print(f"Duration Score: {durationScore}")
    
    totalScoreWeight = {
        "pre": 0.5,
        "mnth": 0.5
    }
    
    if durationScore == 0.0:
        totalScoreWeight["pre"] += 0.3
        totalScoreWeight["mnth"] = 0.0
        
    totalScore = totalScoreWeight["pre"] * preScore + totalScoreWeight["mnth"] * durationScore

    print("---------------")
    
    return min(totalScore, 1.0)

