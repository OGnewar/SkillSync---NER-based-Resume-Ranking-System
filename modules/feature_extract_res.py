import spacy
import re

# Load SpaCy NER model and Sentence BERT model
res_spacy_model_path = "assets/Res_Model/output/model-best"
res_ner_model = spacy.load(res_spacy_model_path)

def res_extract_features(text):

    doc = res_ner_model(text)
    
    expRole = ", ".join(ent.text for ent in doc.ents if ent.label_ == "EXP_ROLE")
    expDuration = ", ".join(ent.text for ent in doc.ents if ent.label_ == "EXP_DURATION")
    
    eduDeg = ", ".join(ent.text for ent in doc.ents if ent.label_ == "EDU_DEGREE")
    eduField = ", ".join(ent.text for ent in doc.ents if ent.label_ == "EDU_FIELD")
    
    lang = ", ".join(ent.text for ent in doc.ents if ent.label_ == "LANG")
    langProf = ", ".join(ent.text for ent in doc.ents if ent.label_ == "LANG_PROF")
    
    features = {
        "name": ", ".join(ent.text for ent in doc.ents if ent.label_ == "NAME"),
        "email": ", ".join(ent.text for ent in doc.ents if ent.label_ == "EMAIL"),
        "linkedin": ", ".join(ent.text for ent in doc.ents if ent.label_ == "LINKEDIN"),
        "dob": ", ".join(ent.text for ent in doc.ents if ent.label_ == "DOB"),
        "experience" : ", ".join(f"{role} ( {duration} )" for role, duration in zip(expRole.split(", "), expDuration.split(", "))),
        "education": ", ".join(f"{degree} in {field}" for degree, field in zip(eduDeg.split(", "), eduField.split(", "))),
        "certification": ", ".join(ent.text for ent in doc.ents if ent.label_ == "CERTIFICATION"),
        "hard": ", ".join(ent.text for ent in doc.ents if ent.label_ == "HARD_SKILLS"),
        "soft": ", ".join(ent.text for ent in doc.ents if ent.label_ == "SOFT_SKILLS"),
        "tools": ", ".join(ent.text for ent in doc.ents if ent.label_ == "TOOLS"),
        "products": ", ".join(ent.text for ent in doc.ents if ent.label_ == "PROD"),
        "sector": ", ".join(ent.text for ent in doc.ents if ent.label_ == "SECTOR"),
        "interests": ", ".join(ent.text for ent in doc.ents if ent.label_ == "INTERESTS"),
        "language" : ", ".join(f"{lg} ( {prof} )" for lg, prof in zip(lang.split(", "), langProf.split(", "))) 
    }
    
    return features