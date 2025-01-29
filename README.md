# SkillSync---NER-based-Resume-Ranking-System

## Major Project - PASBCT077

This project was created by:

- [Saujanya Shrestha (PAS077BCT036)](https://github.com/OGnewar)
- [Dipak Poudel      (PAS077BCT019)](https://github.com/Dipak-Poudel-10)
- [Anish Dahal       (PAS077BCT005)](https://github.com/anish77777)

## Setup Guide

This guide is to help you set this app up.

1. **Clone the repository** on your local device using the command below:
```
git clone https://github.com/OGnewar/SkillSync---NER-based-Resume-Ranking-System.git
```

2. **Set up a virtual environment** on your device and **activate it**:
```
python -m venv env
env/Scripts/activate
```

3. **Install the necessary libraries and packages**:
```
pip install flask
pip install werkzeug
pip install transformers
pip install sentence-transformers
pip install spacy
pip install numpy
pip install spacy-transformers
pip install pypdf2
pip install pypdf
pip install torch
pip install thinc
```

4. **Download the spaCy language model**:
```
python -m spacy download en_core_web_trf
```

5. **Download the models** from the link below and keep it in the assets folder of your local repository:
[NER Model Link](https://drive.google.com/drive/folders/1z_knxWITdAtcZWyIQwGgv-7BwuCEKEhO?usp=sharing)

6. **Run the code** below to fire up the app:
```
python app.py
```

7. **Deactivate the virtual environment** after you're done with your work:
```
deactivate
```