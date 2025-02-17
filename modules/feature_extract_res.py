import spacy
import re

# Load SpaCy NER model and Sentence BERT model
res_spacy_model_path = "assets/Res_Model/output/model-best"
res_ner_model = spacy.load(res_spacy_model_path)

'''
degree_patterns = [
    # Doctorate Degrees
    r"(Ph\.D\.|D\.Phil|Ed\.D\.|Sc\.D\.|D\.Sc\.|D\.B\.A\.|D\.M\.A\.|Psy\.D\.|Th\.D\.) in ([A-Za-z\s]+)",
    r"(Doctorate|Doctor|Doctor of Philosophy|Doctor of Education|Doctor of Science|Doctor of Business Administration) in ([A-Za-z\s]+)",
    
    # Master's Degrees
    r"(M\.S\.|M\.A\.|M\.Ed\.|M\.Eng\.|MBA|MFA|MPH|MSW|MSc|MPhil) in ([A-Za-z\s]+)",
    r"(Master|Master's|Master of Science|Master of Arts|Master of Business Administration|Master of Education|Master of Fine Arts|Master of Public Health) in ([A-Za-z\s]+)",

    # Bachelor's Degrees
    r"(B\.S\.|B\.A\.|BBA|B\.Eng\.|BFA|B\.Tech\.|BCom|BEd) in ([A-Za-z\s]+)",
    r"(Bachelor|Bachelor's|Bachelor of Science|Bachelor of Arts|Bachelor of Business Administration|Bachelor of Education|Bachelor of Engineering) in ([A-Za-z\s]+)",

    # Associate Degrees
    r"(A\.S\.|A\.A\.) in ([A-Za-z\s]+)",
    r"(Associate|Associate's|Associate of Science|Associate of Arts) in ([A-Za-z\s]+)",

    # **Separate Diplomas & Certifications**
    r"(Diploma|Certificate|Degree) in ([A-Za-z\s]+)"
]'''

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
    
    '''
    expRole = ", ".join(ent.text for ent in doc.ents if ent.label_ == "EXP_ROLE")
    expDuration = ", ".join(ent.text for ent in doc.ents if ent.label_ == "EXP_DURATION")
    
    #Education
    eduDeg = []
    eduField = []
    for pattern in degree_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            eduDeg.append(match[0])
            eduField.append(match[1])
    # If regex found nothing, fall back to NER
    if not eduDeg:
        eduDeg = [ent.text for ent in doc.ents if ent.label_ == "EDU_DEGREE"]
    if not eduField:
        eduField = [ent.text for ent in doc.ents if ent.label_ == "EDU_FIELD"]
    # Join extracted values
    eduDeg = ", ".join(eduDeg)
    eduField = ", ".join(eduField)
    
    lang = ", ".join(ent.text for ent in doc.ents if ent.label_ == "LANG")
    langProf = ", ".join(ent.text for ent in doc.ents if ent.label_ == "LANG_PROF")
    
    features = {
        "name": ", ".join(ent.text for ent in doc.ents if ent.label_ == "NAME"),
        "email": ", ".join(ent.text for ent in doc.ents if ent.label_ == "EMAIL"),
        "linkedin": ", ".join(ent.text for ent in doc.ents if ent.label_ == "LINKEDIN"),
        "dob": ", ".join(ent.text for ent in doc.ents if ent.label_ == "DOB"),
        "experience" : ", ".join(f"{role} ( {duration} )" for role, duration in zip(expRole.split(", "), expDuration.split(", "))),
        
        "education": ", ".join(f"{degree} in {field}" if field else degree for degree, field in zip(eduDeg.split(", "), eduField.split(", "))),
        
        "certification": ", ".join(ent.text for ent in doc.ents if ent.label_ == "CERTIFICATION"),
        "hard": ", ".join(ent.text for ent in doc.ents if ent.label_ == "HARD_SKILLS"),
        "soft": ", ".join(ent.text for ent in doc.ents if ent.label_ == "SOFT_SKILLS"),
        "tools": ", ".join(ent.text for ent in doc.ents if ent.label_ == "TOOLS"),
        "products": ", ".join(ent.text for ent in doc.ents if ent.label_ == "PROD"),
        "sector": ", ".join(ent.text for ent in doc.ents if ent.label_ == "SECTOR"),
        "interests": ", ".join(ent.text for ent in doc.ents if ent.label_ == "INTERESTS"),
        "language" : ", ".join(f"{lg} ( {prof} )" for lg, prof in zip(lang.split(", "), langProf.split(", "))) 
    }'''
    
    return features