def displayJobFeats(job):
    
    title = job[0]
    company = job[1]
    expRoles = job[2]
    expMnths = job[3]
    expFields = job[4]
    eduDegs = job[5]
    eduFields = job[6]
    hards = job[7]
    softs = job[8]
    tools = job[9]
    products = job[10]
    sectors = job[11]
    langs = job[12]
    langProfs = job[13]
    certifications = job[14]
    
    jobFeatures = {
        "title": ", ".join(title or ["Unavailable"]),
        "company": ", ".join(company or ["Unavailable"]),
        "experience": "A total of " + f"{expMnths/12} years ( {expMnths} months )" + " in fields like: " + ", ".join(expFields or ["Unavailable"]) + " in roles of: " + ", ".join(expRoles or ["Unavailable"]),
        "education": " or ".join(eduDegs or ["Unavailable"]) + " in fields like: " + ", ".join(eduFields or ["Unavailable"]),
        "hards": ", ".join(hards or ["Unavailable"]),
        "softs": ", ".join(softs or ["Unavailable"]),
        "tools": ", ".join(tools or ["Unavailable"]),
        "products": ", ".join(products or ["Unavailable"]),
        "sectors": ", ".join(sectors or ["Unavailable"]),
        "language": " or ".join(langProfs or ["Unavailable"]) + " proficiency in languages like: " + ", ".join(langs or ["Unavailable"]),
        "certifications": ", ".join(certifications or ["Unavailable"])
    }
    
    return jobFeatures