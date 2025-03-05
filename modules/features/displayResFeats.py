from itertools import zip_longest

def displayResFeats(res):
    
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
        "name": ", ".join(name or ["Unavailable"]),
        "email": ", ".join(email or ["Unavailable"]),
        "links": ", ".join(links or ["Unavailable"]),
        "phone": ", ".join(phone or ["Unavailable"]),
        "dob": ", ".join(dob or ["Unavailable"]),

        "experience": ", ".join(f"{role or 'Unavailable Role'} ( {duration or 'Unavailable Duration'} ) ( {months or 'Unavailable Months'} )" for role, duration, months in zip_longest(expRoles, expYrs, expMonths)) + " in fields like " + ", ".join(f"{field or 'Unavailable Field'}" for field in expFields),

        "education": ", ".join(f"{deg or 'Unavailable Degree'} in {field or 'Unavailable Field'}" for deg, field in zip(eduDegs, eduFields)),
        
        "hards": ", ".join(hards or ["Unavailable"]),
        "softs": ", ".join(softs or ["Unavailable"]),
        "tools": ", ".join(tools or ["Unavailable"]),
        "products": ", ".join(products or ["Unavailable"]),
        "sectors": ", ".join(sectors or ["Unavailable"]),
        "interests": ", ".join(interests or ["Unavailable"]),

        "language": ", ".join(f"{lang or 'Unavailable'} ( {prof or 'Unavailable'} )" for lang, prof in zip_longest(langs, langProfs, fillvalue="___")),
        
        "certifications": ", ".join(certifications or ["Unavailable"])
    }
    
    return resFeatures