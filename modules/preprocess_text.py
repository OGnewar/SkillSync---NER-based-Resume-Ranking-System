def preprocess_text(text):
    preprocessed_text = text.strip()
    normalized_text = ' '.join(preprocessed_text.split())
    return normalized_text