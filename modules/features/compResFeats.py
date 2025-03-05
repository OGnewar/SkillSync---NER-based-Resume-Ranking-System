def compResFeats(res):
    
    name = res[0]
    email = res[1]
    links = res[2]
    phone = res[3]
    dob = res[4]
    expRoles = res[5]
    expYrs = res[6]
    expFields = res[7]
    eduDegs = res[8]
    eduFields = res[9]
    hards = res[10]
    softs = res[11]
    tools = res[12]
    products = res[13]
    sectors = res[14]
    interests = res[15]
    langs = res[16]
    langProfs = res[17]
    certifications = res[18]
    expMnths = res[19]
    expMonths = res[20]
    
    resFeatures = {
        "applicant": {
            "name": name,
            "email": email,
            "links": links,
            "phone": phone,
            "dob": dob,
            "interests": interests
        },
        "experience": {
            "expRoles": expRoles,
            "expYrs": expYrs,
            "expMonths": expMonths,
            "expMnths": expMnths,
            "expFields": expFields,
            "eduFields": eduFields,
            "hards": hards,
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
    
    return resFeatures