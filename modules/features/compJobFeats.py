def compJobFeats(job):
    
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
    expYrs = job[15]
    expMonths = job[16]
    
    jobFeatures = {
        "job": {
            "title": title,
            "company": company
        },
        "experience": {
            "title": title,
            "expRoles": expRoles,
            "expYrs": expYrs,
            "expMonths": expMonths,
            "expMnths": expMnths,
            "expFields": expFields,
            "eduFields": eduFields,
            "hards": hards,
            "softs": softs,
            "tools": tools,
            "products": products,
            "sectors": sectors
        },
        "education": {
            "eduDegs": eduDegs,
            "eduFields": eduFields,
            "expFields": expFields,
            "certifications": certifications
        },
        "skills": {
            "hards": hards,
            "softs": softs,
            "tools": tools,
            "products": products,
            "expFields": expFields,
            "eduFields": eduFields
        },
        "language": {
            "langs": langs,
            "langProfs": langProfs
        }
    }
    
    return jobFeatures