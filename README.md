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

### 1. Clone the Repository:
```
git clone https://github.com/OGnewar/SkillSync---NER-based-Resume-Ranking-System.git
```

<br>

### 2.  Set and Activate the Virtual Environment:
```
python -m venv env
env/Scripts/activate
```

<br>

### 3.  Install the Packages:
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

<br>

### 4.  Download the spaCy language model:
```
python -m spacy download en_core_web_trf
```

<br>

### 5. Setup the Custom NER Model:

Download the models from the link below and keep it in the assets folder of your local repository:

<br>

[NER Model Link](https://drive.google.com/drive/folders/1z_knxWITdAtcZWyIQwGgv-7BwuCEKEhO?usp=sharing)

<br>

### 6. Login or No Login?

If you want to run the app with the login with google feature, follow from step 8 onwards; else go to step 7.

<br>

### 7. No Login:

Go to base.html and remove or comment out from line 46 to line 50 and run the command:
```
python app_no_login.py
```

<br>

### 8. Obtain your OAuth Credentials:

- Go to the Google Cloud Console website.
- Create a new project.
- Go to APIs & Services > Library
- Enable Google+ API.
- Go to APIs & Services > Credentials
- Click Create Credentials > OAuth Client ID
- Select Application Type.
- Name your client.
- Add Authorized JavaScript Origins as:
```
http://localhost:5000
```
- Add Authorized redirect URLs
```
http://127.0.0.1:5000/login/callback
```
- Download the json file containing your client id and secret

<br>

## With Login
### 9. Add Environment Variables:

Create a .env file in your local directory and place your client id and secret:
```
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client-secret
SECRET_KEY=your_secret_key
```
<br>

### 10. Load the Env Files:

Load the keys from .env file placing it in your app.py:
```
from dotenv import load_dotenv
load_dotenv()
```

<br>

### 11. Run the App:

Run the code below to fire up the app:
```
python app.py
```

<br>

### 12. Deactivate the Virtual Environment:

Deactivate the virtual environment after you're done with your work:
```
deactivate
```