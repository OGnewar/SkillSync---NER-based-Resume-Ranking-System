from sentence_transformers import SentenceTransformer, util

# Load the SBERT model
model = SentenceTransformer('nli-roberta-base-v2')

def cosine_similarity(text1, text2):
    if not text1 or not text2:
        return 0
    embeddings = model.encode([text1, text2], convert_to_tensor=True)
    return util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()

def education_similarity(job, res):
    # Extract education details
    jobEdu = job.get("education", {})
    resEdu = res.get("education", {})
    
    jobFld = jobEdu.get("eduFields", []) + jobEdu.get("expFields", [])
    resFld = resEdu.get("eduFields", [])
    jobDeg = jobEdu.get("eduDegs", [])
    resDeg = resEdu.get("eduDegs", [])
    jobCert = jobEdu.get("certifications", [])
    resCert = resEdu.get("certifications", [])
    
    # print("EDUCATION SIMILARITY")
    # print("--------------")
    # print(f"Job Field: {jobFld}")
    # print(f"Resume Field: {resFld}")
    # print(f"Job Degrees: {jobDeg}")
    # print(f"Resume Degrees: {resDeg}")
    # print(f"Job Certifications: {jobCert}")
    # print(f"Resume Certifications: {resCert}")
    
    jobFldStr = ", ".join(jobFld)
    resFldStr = ", ".join(resFld)
    jobCertStr = ", ".join(jobCert)
    resCertStr = ", ".join(resCert)
    
    fldScore = cosine_similarity(jobFldStr, resFldStr)
    certScore = cosine_similarity(jobCertStr, resCertStr)
    
    # print(f"Field Score: {fldScore}")
    # print(f"Certification Score: {certScore}")

    degPriority = {
        "Undergraduate": 1,
        "Diploma": 1.5, "Graduate": 1.5,
        "Bachelor": 2, "Bachelor's": 2, "Bachelor’s degree": 2, "B.S.": 2, "B.Sc": 2, "B.S": 2, "B.Tech": 2, "Bachelors degree": 2, "Postgraduate": 2,
        "Master's": 3, "Masters": 3,
        "Ph.D": 4, "Ph.D.": 4
    }
    
    jobDegPrt = [degPriority.get(deg, -1) for deg in jobDeg]
    resDegPrt = [degPriority.get(deg, -1) for deg in resDeg]
    
    # print(f"Job Degrees: {jobDegPrt}")
    # print(f"Resume Degrees: {resDegPrt}")
    
    if not jobDegPrt or not resDegPrt:
        return 0.0
    
    minJobDeg = min(jobDegPrt)
    maxResDeg = max(resDegPrt)
    
    degScore = 0.0
    if fldScore > 0.5:
        if maxResDeg >= minJobDeg:
            degScore = 1.0
        else:
            diff = minJobDeg - maxResDeg
            degScore = max(0, 1.0 - (diff / 3))  # Normalize difference with max priority 3
    else:
        if maxResDeg >= minJobDeg:
            degScore = 1.0 /  2
        else:
            diff = minJobDeg - maxResDeg
            degScore = max(0, 1.0 - (diff / 3))
            degScore /= 2
            
    # print(f"Degree Score: {degScore}")
    
    weights = {
        "field": 0.5,
        "degree": 0.4,
        "cert": 0.1
    }
    
    if not jobCert:
        weights["field"] += 0.05
        weights["degree"] += 0.05
        
    score = weights["field"] * fldScore + weights["degree"] * degScore + weights["cert"] * certScore

    # print("---------------")
    
    return round(score, 4)

