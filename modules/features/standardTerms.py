# config/standardized_terms.py

standardTerms = {
    "hards": {
        "CNN": "Convolutional Neural Network (CNN)",
        "CNNs": "Convolutional Neural Network (CNN)",
        "convolutional neural network": "Convolutional Neural Network (CNN)",
        "convolutional neural networks": "Convolutional Neural Network (CNN)",
        "RNN": "Recurrent Neural Network (RNN)",
        "GPU": "Graphics Processing Unit",
        "NLP": "Natural Language Processing",
        "ML": "Machine Learning",
        "AI": "Artificial Intelligence"
    },
    "tools": {
        "PS": "Photoshop",
        "MS Excel": "Microsoft Excel",
        "PyTorch": "PyTorch",
        "TF": "TensorFlow", 
        "SAS": "Statistical Analysis System"
    },
    "products": {
        "AWS": "Amazon Web Services",
        "GCP": "Google Cloud Platform",
        "Azure": "Microsoft Azure"
    },
    "eduDegs": {
        "B.S": "Bachelor of Science",
        "B.Sc": "Bachelor of Science",
        "M.S": "Master of Science",
        "M.Sc": "Master of Science",
        "PhD": "Doctor of Philosophy",
        "Bachelors": "Bachelor's",
        "Masters degree": "Master's"
    },
    "expFields": {
        "IT": "Information Technology",
        "IT Management": "Information Technology",
        "IT management": "Information Technology"
    }
}

# Function to standardize extracted values
def standardizeTerms(entity_list, category):
    standard_dict = standardTerms.get(category, {})

    # Maintain order while replacing terms
    standardized_list = [standard_dict.get(value, value) for value in entity_list]

    return standardized_list if standardized_list else []

