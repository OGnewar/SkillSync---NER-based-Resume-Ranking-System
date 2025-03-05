import spacy
import re

# Load SpaCy NER model and Sentence BERT model
res_spacy_model_path = "assets/Res_Model/output/model-best"
res_ner_model = spacy.load(res_spacy_model_path)

def extract_res_features(text):

    doc = res_ner_model(text)
    
    resFeatures = {
        "applicant": {   
            "name": [ent.text for ent in doc.ents if ent.label_ == "NAME"],
            "email": [ent.text for ent in doc.ents if ent.label_ == "EMAIL"],
            "linkedin": [ent.text for ent in doc.ents if ent.label_ == "LINKEDIN"],
            "dob": [ent.text for ent in doc.ents if ent.label_ == "DOB"],
            "interests": [ent.text for ent in doc.ents if ent.label_ == "INTEREST"]
            },
        "experience":{
            "expRole": [ent.text for ent in doc.ents if ent.label_ == "EXP_ROLE"],
            "expYrs": [ent.text for ent in doc.ents if ent.label_ == "EXP_DURATION"],
            "eduField": [ent.text for ent in doc.ents if ent.label_ == "EDU_FIELD"],
            "hard": [ent.text for ent in doc.ents if ent.label_ == "HARD_SKILLS"],
            "tools": [ent.text for ent in doc.ents if ent.label_ == "TOOLS"],
            "products": [ent.text for ent in doc.ents if ent.label_ == "PROD"],
            "sector": [ent.text for ent in doc.ents if ent.label_ == "SECTOR"]
            },
        "education":{   
            "eduDeg": [ent.text for ent in doc.ents if ent.label_ == "EDU_DEGREE"],
            "eduField": [ent.text for ent in doc.ents if ent.label_ == "EDU_FIELD"],
            "certification": [ent.text for ent in doc.ents if ent.label_ == "CERTIFICATION"]
            },
        "skills": {
            "hard": [ent.text for ent in doc.ents if ent.label_ == "HARD_SKILLS"],
            "soft": [ent.text for ent in doc.ents if ent.label_ == "SOFT_SKILLS"],
            "tools": [ent.text for ent in doc.ents if ent.label_ == "TOOLS"],
            "products": [ent.text for ent in doc.ents if ent.label_ == "PROD"],
            "eduField": [ent.text for ent in doc.ents if ent.label_ == "EDU_FIELD"],
            },
        "language": {
            "lang": [ent.text for ent in doc.ents if ent.label_ == "LANG"],
            "langProf": [ent.text for ent in doc.ents if ent.label_ == "LANG_PROF"]
        }
    }
    
    return resFeatures