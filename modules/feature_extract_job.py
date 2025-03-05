import spacy

# Load SpaCy NER model and Sentence BERT model
job_spacy_model_path = "assets/JD_Model/output/model-best"
job_ner_model = spacy.load(job_spacy_model_path)

def job_extract_features(text):

    doc = job_ner_model(text)
    
    expYrs = ", ".join(ent.text for ent in doc.ents if ent.label_ == "EXP_YRS")
    expField = ", ".join(ent.text for ent in doc.ents if ent.label_ == "EXP_FIELD")
    expRole = ", ".join(ent.text for ent in doc.ents if ent.label_ == "EXP_ROLE")
    
    eduDeg = ", ".join(ent.text for ent in doc.ents if ent.label_ == "EDU_DEGREE")
    eduField = ", ".join(ent.text for ent in doc.ents if ent.label_ == "EDU_FIELD")
    
    lang = ", ".join(ent.text for ent in doc.ents if ent.label_ == "LANGUAGE")
    langProf = ", ".join(ent.text for ent in doc.ents if ent.label_ == "LANG_PROF")
    
    features = {
        "title": ", ".join(ent.text for ent in doc.ents if ent.label_ == "JOB_TITLE"),
        "company": ", ".join(ent.text for ent in doc.ents if ent.label_ == "COMPANY_NAME"),
        "experience" : ", ".join(f"{yrs} in {field} as {role}" for yrs, field, role in zip(expYrs.split(", "), expField.split(", "), expRole.split(", "))),
        "education" : ", ".join(f"{degree} in {field}" for degree, field in zip(eduDeg.split(", "), eduField.split(", "))),  
        "sector": ", ".join(ent.text for ent in doc.ents if ent.label_ == "SECTOR"),      
        "certification": ", ".join(ent.text for ent in doc.ents if ent.label_ == "CERTIFICATION"),
        "hard": ", ".join(ent.text for ent in doc.ents if ent.label_ == "HARD_SKILLS"),
        "soft": ", ".join(ent.text for ent in doc.ents if ent.label_ == "SOFT_SKILLS"),
        "tools": ", ".join(ent.text for ent in doc.ents if ent.label_ == "TOOLS"),
        "products": ", ".join(ent.text for ent in doc.ents if ent.label_ == "PROD"),
        "language" : ", ".join(f"{lg} ( {prof} )" for lg, prof in zip(lang.split(", "), langProf.split(", ")))
    }
    
    return features
    