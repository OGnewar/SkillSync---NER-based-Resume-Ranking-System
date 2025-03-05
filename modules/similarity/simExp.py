'''import re
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

# Load SBERT model
model = SentenceTransformer("nli-roberta-base-v2")

def cosine_similarity(text1, text2):
    """Compute cosine similarity using SBERT embeddings."""
    if not text1 or not text2:  # Handle empty or None values
        return 0
    embeddings = model.encode([text1, text2], convert_to_tensor=True)
    return util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()

def extract_months(exp_text):
    """Convert experience duration text into total months."""
    if not exp_text:  # Handle None values
        return 0

    exp_text = exp_text.lower()

    # Case 1: Direct year/month format (e.g., "3 years", "2.5 years", "6 months", "at least 3 years", "3+ years")
    year_match = re.search(r"(\d+(\.\d+)?)(?:\s*\+|\s*at least)?\s*(?:year|yr)", exp_text)
    month_match = re.search(r"(\d+)(?:\s*\+|\s*at least)?\s*month", exp_text)

    years = float(year_match.group(1)) if year_match else 0
    months = int(month_match.group(1)) if month_match else 0

    total_months = int(years * 12 + months)

    # Case 2: Date range format (e.g., "2018 to 2019", "2020-Present")
    date_match = re.findall(r"(\d{4})", exp_text)
    if len(date_match) == 2:
        start_year = int(date_match[0])
        end_year = datetime.now().year if "present" in exp_text or "current" in exp_text else int(date_match[1])
        total_months = (end_year - start_year) * 12  # Approximate
    elif len(date_match) == 1 and ("present" in exp_text or "current" in exp_text):
        # Handle "2020 - Present" cases
        start_year = int(date_match[0])
        end_year = datetime.now().year
        total_months = (end_year - start_year) * 12

    return max(total_months, 1)  # Ensure at least 1 month

def experience_similarity(jobExp, resExp):
    """Compute similarity score between job and resume experience."""
    job_details = jobExp.get("experience", {})
    resume_details = resExp.get("experience", {})

    # Ensure required fields exist
    job_titles = job_details.get("title", [])
    resume_roles = resume_details.get("expRole", [])
    if not job_titles or not resume_roles:
        return 0  # If no job titles or resume roles, no similarity can be computed
    
    print(f"Job Titles: {job_titles}")
    print(f"Resume Roles: {resume_roles}")

    # Step 1: Compare Job Title with Resume Roles
    title_scores = [
        cosine_similarity(job_title, role) for job_title in job_titles for role in resume_roles
    ]

    max_title_similarity = max(title_scores) if title_scores else 0

    # Multiplication Factor (importance weight based on title match)
    multiplication_factor = max_title_similarity ** 2  

    # Step 2: Compare Experience Durations (Convert to Months)
    job_months_list = [extract_months(exp) for exp in job_details.get("expYrs", [])]
    resume_months_list = [extract_months(exp) for exp in resume_details.get("expDuration", [])]

    # Avoid zero division and compute duration similarity
    if job_months_list and resume_months_list:
        duration_scores = [
            1 - abs(job_months - res_months) / max(job_months, res_months) if max(job_months, res_months) > 0 else 0
            for job_months in job_months_list for res_months in resume_months_list
        ]
        max_duration_similarity = max(duration_scores) if duration_scores else 0
    else:
        max_duration_similarity = 0

    # Weighted experience similarity score
    experience_similarity_score = max_duration_similarity * multiplication_factor

    # Step 3: Compare Job Experience Role (if present)
    role_scores = [
        cosine_similarity(job_role, resume_role)
        for job_role in job_details.get("expRole", [])
        for resume_role in resume_details.get("expRole", [])
    ]
    max_role_similarity = max(role_scores) if role_scores else 0

    # Step 4: Compare Sector (if present)
    sector_scores = [
        cosine_similarity(job_sector, resume_sector)
        for job_sector in job_details.get("sector", [])
        for resume_sector in resume_details.get("sector", [])
    ]
    max_sector_similarity = max(sector_scores) if sector_scores else 0

    # Final Score Calculation with Weighted Contributions
    overall_score = (
        experience_similarity_score +
        (0.2 * max_role_similarity) +
        (0.1 * max_sector_similarity)
    )

    # Normalize score between 0 and 1
    return min(overall_score, 1.0)'''
    
'''import re
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

# Load SBERT model
model = SentenceTransformer("nli-roberta-base-v2")

def cosine_similarity(text1, text2):
    """Compute cosine similarity using SBERT embeddings."""
    if not text1 or not text2:  # Handle empty or None values
        return 0.0
    embeddings = model.encode([text1, text2], convert_to_tensor=True)
    return util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()

def extract_months(exp_text):
    """Convert experience duration text into total months."""
    if not exp_text:  # Handle None values
        return 0

    exp_text = exp_text.lower()

    # Case 1: Direct year/month format (e.g., "3 years", "2.5 years", "6 months", "at least 3 years", "3+ years")
    year_match = re.search(r"(\d+(\.\d+)?)(?:\s*\+|\s*at least)?\s*(?:year|yr)", exp_text)
    month_match = re.search(r"(\d+)(?:\s*\+|\s*at least)?\s*month", exp_text)

    years = float(year_match.group(1)) if year_match else 0
    months = int(month_match.group(1)) if month_match else 0

    total_months = int(years * 12 + months)

    # Case 2: Date range format (e.g., "2018 to 2019", "2020-Present")
    date_match = re.findall(r"(\d{4})", exp_text)
    if len(date_match) == 2:
        start_year = int(date_match[0])
        end_year = datetime.now().year if "present" in exp_text or "current" in exp_text else int(date_match[1])
        total_months = (end_year - start_year) * 12  # Approximate
    elif len(date_match) == 1 and ("present" in exp_text or "current" in exp_text):
        # Handle "2020 - Present" cases
        start_year = int(date_match[0])
        end_year = datetime.now().year
        total_months = (end_year - start_year) * 12

    return max(total_months, 1)  # Ensure at least 1 month

def experience_similarity(jobExp, resExp):
    """Compute similarity score between job and resume experience."""
    job_details = jobExp.get("experience", {})
    resume_details = resExp.get("experience", {})
    
    print(f"Job Experience: {job_details}")
    print(f"Resume Experience: {resume_details}")

    # Ensure required fields exist
    job_titles = job_details.get("title", [])
    resume_roles = resume_details.get("expRole", [])
    if not job_titles or not resume_roles:
        return 0.0  # If no job titles or resume roles, no similarity can be computed

    print(f"Job Title: {job_titles}")
    print(f"Resume Roles: {resume_roles}")
    
    # Step 1: Compare Job Title with Resume Roles
    title_scores = [
        cosine_similarity(job_title, role) for job_title in job_titles for role in resume_roles
    ]
    max_title_similarity = max(title_scores) if title_scores else 0.0
    
    print(f"Title Similarity = {title_scores}")

    # Step 2: Compare Experience Durations (Convert to Months) - Only if Title Similarity > 0.5
    job_months_list = [extract_months(exp) for exp in job_details.get("expYrs", [])]
    resume_months_list = [extract_months(exp) for exp in resume_details.get("expDuration", [])]
    
    print(f"Job Months = {job_months_list}")
    print(f"Resume Months = {resume_months_list}")

    duration_similarity = 0.0
    if max_title_similarity > 0.5 and job_months_list and resume_months_list:
        duration_scores = [
            1 - abs(job_months - res_months) / max(job_months, res_months) if max(job_months, res_months) > 0 else 0
            for job_months in job_months_list for res_months in resume_months_list
        ]
        duration_similarity = max(duration_scores) if duration_scores else 0.0

    print(f"Duration Similarity = {duration_similarity}")

    # Step 3: Compare Job Experience Role (if present)
    job_roles = job_details.get("expRole", [])
    role_scores = [
        cosine_similarity(job_role, resume_role)
        for job_role in job_roles
        for resume_role in resume_details.get("expRole", [])
    ]
    max_role_similarity = max(role_scores) if role_scores else 0.0
    
    print(f"Role Similarity = {max_role_similarity}")

    # Step 4: Compare Sector (if present)
    job_sectors = job_details.get("sector", [])
    sector_scores = [
        cosine_similarity(job_sector, resume_sector)
        for job_sector in job_sectors
        for resume_sector in resume_details.get("sector", [])
    ]
    max_sector_similarity = max(sector_scores) if sector_scores else 0.0
    
    print(f"Sector Similarity = {max_sector_similarity}")

    # Step 5: Adjust Weights Based on Missing Job Fields
    total_weight = 1.0  # Ensure score does not exceed 1.0
    title_weight = 0.4
    duration_weight = 0.3 if max_title_similarity > 0.5 else 0.0
    role_weight = 0.2 if job_roles else 0.0
    sector_weight = 0.1 if job_sectors else 0.0

    # If "expRole" is missing, redistribute its 20% weight
    if not job_roles:
        title_weight += 0.1
        duration_weight += 0.1
        sector_weight += 0.05

    # If "sector" is missing, redistribute its 10% weight
    if not job_sectors:
        title_weight += 0.05
        duration_weight += 0.05
        role_weight += 0.05

    # Final Score Calculation with Adjusted Weights
    overall_score = (
        (title_weight * max_title_similarity) +
        (duration_weight * duration_similarity) +
        (role_weight * max_role_similarity) +
        (sector_weight * max_sector_similarity)
    )

    # Ensure the max score remains 1.0
    return min(overall_score, total_weight)'''


# Sample Test Data
'''
jobFeatures = {
    "experience": {
        "title": ["Software Engineer"],
        "expYrs": ["3 years", "4+ years"],
        "expRole": ["Backend Developer", "Software Engineer"],
        "sector": ["IT", "Software Development"]
    }
}

resFeatures = {
    "experience": {
        "expRole": ["Software Developer", "Backend Engineer"],
        "expDuration": ["3.5 years", "5 years"],
        "sector": ["Technology", "Software Engineering"]
    }
}
'''

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

'''def extract_months(text):
    text = text.lower().strip()
    current_date = datetime.today()
    
    # Pattern for direct year ranges (e.g., "2013-2020" or "2013 -2019")
    year_range_match = re.match(r"(\d{4})\s*[-–]\s*(\d{4}|present|ongoing)", text)
    if year_range_match:
        start_year = int(year_range_match.group(1))
        end_year = current_date.year if "present" in year_range_match.group(2) or "ongoing" in year_range_match.group(2) else int(year_range_match.group(2))
        return (end_year - start_year) * 12
    
    # Pattern for month-year ranges (e.g., "Nov 2015 to Dec 2016")
    date_range_match = re.match(r"(\w{3,9})\s*(\d{4})\s*to\s*(\w{3,9}|present|ongoing)\s*(\d{4})?", text)
    if date_range_match:
        start_date = parse(f"{date_range_match.group(1)} {date_range_match.group(2)}")
        end_date = current_date if "present" in text or "ongoing" in text else parse(f"{date_range_match.group(3)} {date_range_match.group(4) or date_range_match.group(2)}")
        return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    
    # Pattern for day/month/year ranges (e.g., "26/10/2013 - 30/05/2025")
    date_slash_match = re.match(r"(\d{1,2}/\d{1,2}/\d{4})\s*-\s*(\d{1,2}/\d{1,2}/\d{4}|present|ongoing)", text)
    if date_slash_match:
        start_date = parse(date_slash_match.group(1))
        end_date = current_date if "present" in text or "ongoing" in text else parse(date_slash_match.group(2))
        return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    
    # Pattern for experience descriptions (e.g., "minimum 3 years", "6+ years")
    exp_year_match = re.search(r"(\d+)\s*(\+?\s*years?|yrs?)", text)
    if exp_year_match:
        return int(exp_year_match.group(1)) * 12
    
    return 0  # If no pattern is matched'''

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
    '''jobMonth = 0.0
    resMonth = 0.0
    for month in jobMonths:
        jobMonth += month
    for month in resMonths:
        resMonth += month'''
        
    #print(f"Total Job Months: {jobMonth}")
    #print(f"Total Resume Months: {resMonth}")
    
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

