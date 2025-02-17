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
    
    '''
    # Extract experience details
    expYrs = [ent.text.strip().replace("•", "").replace("", "") for ent in doc.ents if ent.label_ == "EXP_YRS"]
    expField = [ent.text.strip() for ent in doc.ents if ent.label_ == "EXP_FIELD"]
    expRole = [ent.text.strip() for ent in doc.ents if ent.label_ == "EXP_ROLE"]

    # Extract education details (remove duplicates)
    eduDeg = list(set(ent.text.strip().replace("\n", " ") for ent in doc.ents if ent.label_ == "EDU_DEGREE"))
    eduField = list(set(ent.text.strip().replace("\n", " ") for ent in doc.ents if ent.label_ == "EDU_FIELD"))

    # Extract languages and proficiency
    lang = [ent.text.strip() for ent in doc.ents if ent.label_ == "LANGUAGE"]
    langProf = [ent.text.strip() for ent in doc.ents if ent.label_ == "LANG_PROF"]

    # Ensure all languages are accounted for, even if they have no proficiency
    language_output = []
    for i in range(len(lang)):
        prof = langProf[i] if i < len(langProf) else ""  # Leave blank instead of "Unknown proficiency"
        language_output.append(f"{lang[i]} ({prof})" if prof else lang[i])  # Only add proficiency if available
    language_result = ", ".join(language_output) if language_output else "Unavailable"

    # Format experience output properly
    experience_entries = []
    num_experiences = max(len(expYrs), len(expField), len(expRole))

    for i in range(num_experiences):
        yrs = expYrs[i] if i < len(expYrs) else "Unknown"
        field = expField[i] if i < len(expField) else "Unknown"
        role = expRole[i] if i < len(expRole) else "Unknown"

        experience_entries.append(f"{yrs} in {field} as {role}")

    # Join formatted experiences
    experience_output = ", ".join(experience_entries) if experience_entries else "Unavailable"

    # Format education output
    if eduDeg:
        degree_part = " or ".join(eduDeg)
    else:
        degree_part = "Relevant degree"

    if eduField:
        field_part = ", ".join(eduField[:-1]) + (" or " + eduField[-1] if len(eduField) > 1 else "")
    else:
        field_part = "related fields"

    education_output = f"{degree_part} in {field_part}"

    # Store extracted features
    features = {
        "title": ", ".join(ent.text for ent in doc.ents if ent.label_ == "JOB_TITLE"),
        "company": ", ".join(ent.text for ent in doc.ents if ent.label_ == "COMPANY_NAME"),
        "experience": experience_output,
        "education": education_output,
        "sector": ", ".join(ent.text for ent in doc.ents if ent.label_ == "SECTOR") or "Unavailable",
        "certification": ", ".join(ent.text.strip() for ent in doc.ents if ent.label_ == "CERTIFICATION"),
        "hard": ", ".join(ent.text.replace("\n", " ").strip() for ent in doc.ents if ent.label_ == "HARD_SKILLS"),
        "soft": ", ".join(ent.text.replace("\n", " ").strip() for ent in doc.ents if ent.label_ == "SOFT_SKILLS"),
        "tools": ", ".join(ent.text for ent in doc.ents if ent.label_ == "TOOLS"),
        "products": ", ".join(ent.text for ent in doc.ents if ent.label_ == "PROD") or "Unavailable",
        "language": language_result
    }'''
    return features
    