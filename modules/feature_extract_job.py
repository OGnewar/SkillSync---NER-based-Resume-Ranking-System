import spacy

# Load SpaCy NER model and Sentence BERT model
job_spacy_model_path = "assets/JD_Model/output/model-best"
job_ner_model = spacy.load(job_spacy_model_path)

def job_extract_features(text):

    doc = job_ner_model(text)
    features = {
        "skills": ", ".join(ent.text for ent in doc.ents if ent.label_ == "SKILLS"),
        "experience": ", ".join(ent.text for ent in doc.ents if ent.label_ == "EXPERIENCE"),
        "education": ", ".join(ent.text for ent in doc.ents if ent.label_ == "EDUCATION"),
        "language": ", ".join(ent.text for ent in doc.ents if ent.label_ == "LANGUAGE"),
    }
    return features