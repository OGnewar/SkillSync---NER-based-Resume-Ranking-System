import spacy

# Load SpaCy NER model and Sentence BERT model
job_spacy_model_path = "assets/JD_Model/output/model-best"
job_ner_model = spacy.load(job_spacy_model_path)

def extract_job_features(text):

    doc = job_ner_model(text)
    
    jobFeatures = {
        "job": {   
            "title": [ent.text for ent in doc.ents if ent.label_ == "JOB_TITLE"],
            "company": [ent.text for ent in doc.ents if ent.label_ == "COMPANY_NAME"]
            },
        "experience":{
            "title": [ent.text for ent in doc.ents if ent.label_ == "JOB_TITLE"],
            "expRole": [ent.text for ent in doc.ents if ent.label_ == "EXP_ROLE"],
            "expYrs": [ent.text for ent in doc.ents if ent.label_ == "EXP_YRS"],
            "expField": [ent.text for ent in doc.ents if ent.label_ == "EXP_FIELD"],
            "eduField": [ent.text for ent in doc.ents if ent.label_ == "EDU_FIELD"],
            "hard": [ent.text for ent in doc.ents if ent.label_ == "HARD_SKILLS"],
            "tools": [ent.text for ent in doc.ents if ent.label_ == "TOOLS"],
            "products": [ent.text for ent in doc.ents if ent.label_ == "PROD"],
            "sector": [ent.text for ent in doc.ents if ent.label_ == "SECTOR"]
            },
        "education":{   
            "eduDeg": [ent.text for ent in doc.ents if ent.label_ == "EDU_DEGREE"],
            "eduField": [ent.text for ent in doc.ents if ent.label_ == "EDU_FIELD"],
            "expField": [ent.text for ent in doc.ents if ent.label_ == "EXP_FIELD"],
            "certification": [ent.text for ent in doc.ents if ent.label_ == "CERTIFICATION"]
            },
        "skills": {
            "hard": [ent.text for ent in doc.ents if ent.label_ == "HARD_SKILLS"],
            "soft": [ent.text for ent in doc.ents if ent.label_ == "SOFT_SKILLS"],
            "tools": [ent.text for ent in doc.ents if ent.label_ == "TOOLS"],
            "products": [ent.text for ent in doc.ents if ent.label_ == "PROD"],
            "expField": [ent.text for ent in doc.ents if ent.label_ == "EXP_FIELD"],
            "eduField": [ent.text for ent in doc.ents if ent.label_ == "EDU_FIELD"]
            },
        "language": {
            "lang": [ent.text for ent in doc.ents if ent.label_ == "LANGUAGE"],
            "langProf": [ent.text for ent in doc.ents if ent.label_ == "LANG_PROF"]
            }
    }

    return jobFeatures