from flask import Flask, request, render_template, redirect, url_for, send_from_directory, session
from werkzeug.utils import secure_filename
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os
from modules.pdf_utils import extract_text_from_pdf
from modules.feature_extract_job import job_extract_features
from modules.feature_extract_res import res_extract_features
from modules.similarity import calculate_similarity
from modules.preprocess_text import preprocess_text
from dotenv import load_dotenv
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Google OAuth configuration
oauth = OAuth(app)

app.config['GOOGLE_CLIENT_ID'] = os.getenv("GOOGLE_CLIENT_ID")
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv("GOOGLE_CLIENT_SECRET")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params={'scope': 'openid email profile'},
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    client_kwargs={'scope': 'openid email profile'},
    redirect_uri='http://127.0.0.1:5000/login/callback',  # Update with your actual callback URL
    server_metadata_url= 'https://accounts.google.com/.well-known/openid-configuration'
)


# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# User class
class User(UserMixin):
    def __init__(self, user_id, name, email):
        self.id = user_id
        self.name = name
        self.email = email

users = {}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# Google Login Route
@app.route("/login")
def login():
    return render_template('login.html')

@app.route('/google-login')
def google_login():
    return google.authorize_redirect(url_for('authorized', _external=True))

@app.route("/login/callback")
def authorized():
    token = google.authorize_access_token()
    if not token:
        return "Access denied"

    # Store token in session
    session["google_token"] = token

    # Get user info
    user_info = google.get("https://www.googleapis.com/oauth2/v1/userinfo").json()
    
    # Create a user session
    user = User(user_info["id"], user_info["name"], user_info["email"])
    users[user_info["id"]] = user
    login_user(user)

    return redirect(url_for("login"))



# Logout Route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop("google_token", None)
    return redirect(url_for("login"))

# Configurations
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def skillSync():
    return render_template('skillsync.html')

@app.route('/intro')
def intro():
    return render_template('intro.html')

#Resume Parse Page
@app.route('/parse_res', methods=['GET', 'POST'])
@login_required
def parse_res():
    if request.method == 'POST':
        resume_file = request.files['resume']
        if not resume_file:
            return "No file selected", 400
        
        # Save the file
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(resume_file.filename))
        resume_file.save(resume_path)
        
        # Extract text from PDF
        resume_text = extract_text_from_pdf(resume_path)
        
        #preprocess res_text
        res_preprocessed_text = preprocess_text(resume_text)

        # Extract features using the custom NER model
        resume_features = res_extract_features(res_preprocessed_text)

        # Redirect to results page with parsed data
        return redirect(url_for('res_details', name=resume_features.get("name", "Unknown"), skills=resume_features.get("skills", ""), 
                                experience=resume_features.get("experience", ""), education=resume_features.get("education", ""), 
                                language=resume_features.get("language", "")))

    return render_template('parse_res.html')

#Display Resume Details
@app.route('/res_details')
def res_details():
    # Get extracted resume data from query parameters
    name = request.args.get("name", "Unknown")
    skills = request.args.get("skills", "Not Available")
    experience = request.args.get("experience", "Not Available")
    education = request.args.get("education", "Not Available")
    language = request.args.get("language", "Not Available")

    return render_template('res_details.html', name=name, skills=skills, experience=experience, education=education, language=language)

#Parse JD Page
@app.route('/parse_job', methods=['GET', 'POST'])
@login_required
def parse_job():
    if request.method == 'POST':
        # Get the uploaded job description file
        job_file = request.files.get('job_description')

        if not job_file:
            return "Please upload a job description file!", 400

        # Save the file
        job_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(job_file.filename))
        job_file.save(job_path)

        # Extract text from PDF
        job_text = extract_text_from_pdf(job_path)
        
        #preprocess job_text
        job_preprocessed_text = preprocess_text(job_text)

        # Extract features using the custom NER model
        job_features = job_extract_features(job_preprocessed_text)

        # Redirect to the parsed job description details page
        return redirect(url_for('job_details', 
                                job_title=job_features.get("name", "Unknown"), 
                                job_skills=job_features.get("skills", ""), 
                                job_experience=job_features.get("experience", ""), 
                                job_education=job_features.get("education", ""), 
                                job_language=job_features.get("language", "")))
    
    return render_template('parse_job.html')

@app.route('/job_details')
def job_details():
    return render_template('job_details.html',job_title=request.args.get('job_title', 'Unknown'),job_skills=request.args.get('job_skills', 'Not Available'),job_experience=request.args.get('job_experience', 'Not Available'),job_education=request.args.get('job_education', 'Not Available'),job_language=request.args.get('job_language', 'Not Available'))


# Route: Ranking page
@app.route('/rank', methods=['GET', 'POST'])
@login_required
def rank():
    if request.method == 'POST':
        # Save job description
        job_file = request.files['job_description']
        job_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(job_file.filename))
        job_file.save(job_path)
        
        # Save resumes
        resumes = request.files.getlist('resumes')
        resume_paths = []
        for resume in resumes:
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(resume.filename))
            resume.save(resume_path)
            resume_paths.append(resume_path)

        # Redirect to results page
        return redirect(url_for('results', job_path=job_path, resumes=','.join(resume_paths)))

    return render_template('rank.html')

# Route: Results page
@app.route('/results')
def results():
    job_path = request.args.get('job_path')
    resume_paths = request.args.get('resumes').split(',')

    # Extract and process job description
    job_text = extract_text_from_pdf(job_path)
    job_features = job_extract_features(job_text)

    # Process resumes and calculate similarity scores
    ranked_resumes = []
    for resume_path in resume_paths:
        resume_text = extract_text_from_pdf(resume_path)
        resume_features = res_extract_features(resume_text)

        # Calculate similarity score
        similarity_score = calculate_similarity(job_features, resume_features)
        ranked_resumes.append((resume_path, similarity_score))

    # Sort resumes by similarity score in descending order
    ranked_resumes.sort(key=lambda x: x[1], reverse=True)

    return render_template('results.html', ranked_resumes=ranked_resumes, job_path=job_path)

@app.route('/view_details')
def view_details():
    job_path = request.args.get('job_path')
    resume_path = request.args.get('resume_path')
    similarity_score = request.args.get('score')

    # Ensure similarity_score is properly converted to float
    try:
        similarity_score = float(similarity_score)
    except (TypeError, ValueError):
        similarity_score = 0.0  # Default if conversion fails

    # Extract job details
    job_text = extract_text_from_pdf(job_path)
    job_features = job_extract_features(preprocess_text(job_text))

    # Extract resume details
    resume_text = extract_text_from_pdf(resume_path)
    resume_features = res_extract_features(preprocess_text(resume_text))

    return render_template('view_details.html', job_features=job_features, resume_features=resume_features, similarity_score=similarity_score)


@app.route('/aboutUs')
def aboutUs():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
