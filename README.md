# SkillSync---NER-based-Resume-Ranking-System

<br>

## Major Project - PASBCT077

<br>

This project was created by:

- [Saujanya Shrestha (PAS077BCT036)](https://github.com/OGnewar)
- [Dipak Poudel      (PAS077BCT019)](https://github.com/Dipak-Poudel-10)
- [Anish Dahal       (PAS077BCT005)](https://github.com/anish77777)

<br>

## Setup Guide

<br>

This guide is to help you set this app up.

<br>

1. **<ins>Clone the repository</ins>** on your local device using the command below:
```
git clone https://github.com/OGnewar/SkillSync---NER-based-Resume-Ranking-System.git
```

<br>

2. **<ins>Set up a virtual environment</ins>** on your device and <ins>**activate it**</ins>:
```
python -m venv env
env/Scripts/activate
```


3. **<ins>Install the necessary libraries and packages</ins>**:
```
python -m pip install --upgrade pip
```
```
pip install - U flask
```
```
pip install -U werkzeug
```
```
pip install -U transformers
```
```
pip install -U sentence-transformers
```
```
pip install -U spacy
```
```
pip install -U numpy
```
```
pip install -U spacy-transformers
```
```
pip install -U pypdf2
```
```
pip install -U pypdf
```
```
pip install -U torch
```
```
pip install -U thinc
```
> You can ignore the two commands below if you're planning to run the app without login with google feature
```
pip install Flask-Login Flask-Session Authlib
```
```
pip install python-dotenv
```


4. **<ins>Download the spaCy language model</ins>**:
```
python -m spacy download en_core_web_trf
```


5. **<ins>Download the models</ins>** from the link below and keep it in the assets folder of your local repository:
[NER Model Link](https://drive.google.com/drive/folders/1z_knxWITdAtcZWyIQwGgv-7BwuCEKEhO?usp=sharing)


6. **<ins>If you want to run the app with the login with google feature, follow from step 8; else go to step 7</ins>**


7. **<ins>Go to base.html and remove or comment out from line 46 to line 50</ins>** and run the command:
```
python app_no_login.py
```


8. **<ins>Obtain your OAuth Credentials</ins>**

    - Create a new project
    - Go to APIs & Services > Library
    - Enable Google+ API
    - Go to APIs & Services > Credentials
    - Click Create Credentials > OAuth Client ID
    - Select Application Type
    - Name your client
    - Add Authorized JavaScript Origins as:
    ```
    http://localhost:5000
    ```
    - Add Authorized redirect URLs
    ```
    http://127.0.0.1:5000/login/callback
    ```
    - Download the json file containing your client id and secret


9. **<ins>Create a .env file in your local directory</ins>** and place your client id and secret:
```
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client-secret
SECRET_KEY=your_secret_key
```


10. **<ins>Load the keys from .env file</ins>** placing it in your app.py:
```
from dotenv import load_dotenv
load_dotenv()
```


11. **<ins>Run the code</ins>** below to fire up the app:
```
python app.py
```


12. **<ins>Deactivate the virtual environment</ins>** after you're done with your work:
```
deactivate
```