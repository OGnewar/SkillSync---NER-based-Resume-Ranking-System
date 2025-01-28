import spacy

# Load SpaCy NER model and Sentence BERT model
res_spacy_model_path = "assets/Res_Model/output/model-best"
res_ner_model = spacy.load(res_spacy_model_path)

def res_extract_features(text):

    doc = res_ner_model(text)
    features = {
        "skills": ", ".join(ent.text for ent in doc.ents if ent.label_ == "SKILLS"),
        "experience": ", ".join(ent.text for ent in doc.ents if ent.label_ == "EXPERIENCE"),
        "education": ", ".join(ent.text for ent in doc.ents if ent.label_ == "EDUCATION"),
        "language": ", ".join(ent.text for ent in doc.ents if ent.label_ == "LANGUAGE"),
    }
    return features