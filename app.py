from flask import Flask, request, render_template, redirect, url_for, send_from_directory, session, flash
from flask_session import Session
from werkzeug.utils import secure_filename
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os
from dotenv import load_dotenv
load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

from modules.exText import extract_text
from modules.similarity.similarity import calculate_similarity
from modules.features.exResFeats import exResFeats
from modules.features.exJobFeats import exJobFeats
from modules.features.displayResFeats import displayResFeats
from modules.features.displayJobFeats import displayJobFeats
from modules.features.compJobFeats import compJobFeats
from modules.features.compResFeats import compResFeats
from functools import wraps
# from config import ADMINS
from flask import send_file
import io

# Initialize Flask app
app = Flask(__name__)

DEFAULT_WEIGHTS = {
    'experience': 0.3,
    'education': 0.2,
    'skill': 0.4,
    'language': 0.1
}

def get_current_weights():
    return session.get('weights', DEFAULT_WEIGHTS)

# Google OAuth configuration
oauth = OAuth(app)

# Configure session to use filesystem (not cookies)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

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
    user_info = google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()
    if not token:
        return "Access denied"

    # Store token in session
    # session["google_token"] = token
    session['user'] = {
        'name': user_info['name'],
        'email': user_info['email'],
        'picture': user_info['picture']  # Store profile picture
    }

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
    session.pop('user', None)
    session.clear()
    return redirect(url_for('login'))  # Redirect back to login page

# Configurations
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    """Check if the file type is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Decorator to restrict access to admins
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('You must be logged in as admin to access this page.', 'danger')
            return redirect(url_for('adminLogin'))
        return f(*args, **kwargs)
    return decorated_function

# Admin login page
@app.route('/admin/adminLogin', methods=['GET', 'POST'])
def adminLogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Logged in successfully as admin.', 'success')
            return redirect(url_for('customize'))
        else:
            flash('Invalid admin credentials.', 'danger')
    return render_template('adminLogin.html')

# Admin logout
@app.route('/admin/adminLogout')
def adminLogout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('skillSync'))

@app.route('/')
def skillSync():
    return render_template('skillsync.html')

@app.route('/intro')
def intro():
    return render_template('intro.html')

# Resume Parse Page
@app.route('/parse_res', methods=['GET', 'POST'])
@login_required
def parse_res():
    if request.method == 'POST':
        resume_file = request.files['resume']

        if not resume_file or resume_file.filename == '':
            flash("No file selected!", "error")
            return redirect(request.url)

        if not allowed_file(resume_file.filename):
            flash("Invalid file format! Please upload a PDF, DOCX, or TXT file.", "error")
            return redirect(request.url)
        
        # Save the file
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(resume_file.filename))
        resume_file.save(resume_path)

        # Extract text from PDF
        resume_text = extract_text(resume_path)

        # Extract features using the custom NER model
        resume_features = exResFeats(resume_text)
        
        # Formatted resume features for display
        resFeatures = displayResFeats(resume_features)
        
        #flash message
        flash('Parsing successful!', 'success')

        #get resume features
        name=resFeatures.get("name", "Unknown")
        email=resFeatures.get("email", "Unknown")
        links=resFeatures.get("links", "Unknown")
        phone = resFeatures.get("phone", "Unknown")
        dob=resFeatures.get("dob", "Unknown")
        experience=resFeatures.get("experience", "Unknown")
        education=resFeatures.get("education", "Unknown")
        certifications=resFeatures.get("certifications", "Unknown")
        hards=resFeatures.get("hards", "Unknown")
        softs=resFeatures.get("softs", "Unknown")
        tools=resFeatures.get("tools", "Unknown")
        products=resFeatures.get("products", "Unknown")
        sectors=resFeatures.get("sectors", "Unknown")
        interests=resFeatures.get("interests", "Unknown")
        language=resFeatures.get("language", "Unknown")
        
        # Redirect to results page with parsed data
        return redirect(url_for('res_details', name=name, email=email, links=links, phone=phone, dob=dob, experience=experience, education=education, certifications=certifications, hards=hards, softs=softs, tools=tools, products=products, sectors=sectors, interests=interests, language=language))

    return render_template('parse_res.html')

#Display Resume Details
@app.route('/res_details')
def res_details():
    # Get extracted resume data from query parameters
    name = request.args.get("name", "Unknown")
    email = request.args.get("email", "Not Available")
    links = request.args.get("links", "Not Available")
    phone = request.args.get("phone", "Not Available")
    dob = request.args.get("dob", "Not Available")
    experience = request.args.get("experience", "Not Available")
    education = request.args.get("education", "Not Available")
    certifications = request.args.get("certifications", "Not Available")
    hards = request.args.get("hards", "Not Available")
    softs = request.args.get("softs", "Not Available")
    tools = request.args.get("tools", "Not Available")
    products = request.args.get("products", "Not Available")
    sectors = request.args.get("sectors", "Not Available")
    interests = request.args.get("interests", "Not Available")
    language = request.args.get("language", "Not Available")

    return render_template('res_details.html', name=name, email=email, links=links, phone=phone, dob=dob, experience=experience, education=education, certifications=certifications, hards=hards, softs=softs, tools=tools, products=products, sectors=sectors, interests=interests, language=language)

#Parse JD Page
@app.route('/parse_job', methods=['GET', 'POST'])
@login_required
def parse_job():
    if request.method == 'POST':
        # Get the uploaded job description file
        job_file = request.files.get('job_description')

        if not job_file or job_file.filename == '':
            flash("No file selected!", "error")
            return redirect(request.url)

        if not allowed_file(job_file.filename):
            flash("Invalid file format! Please upload a PDF, DOCX, or TXT file.", "error")
            return redirect(request.url)

        # Save the file
        job_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(job_file.filename))
        job_file.save(job_path)

        # Extract text from PDF
        job_text = extract_text(job_path)

        # Extract features using the custom NER model
        job_features = exJobFeats(job_text)
        
        # Formatted job features
        jobFeatures = displayJobFeats(job_features)
        
        # Flash a success message to show after redirect
        flash('Parsing Successful!', 'success')

        #Get job features
        title=jobFeatures.get("title", "Unknown")
        company=jobFeatures.get("company", "Unknown") 
        experience=jobFeatures.get("experience", "Unknown")
        education=jobFeatures.get("education", "Unknown")
        certifications=jobFeatures.get("certifications", "Unknown")
        sectors=jobFeatures.get("sectors", "Unknown")
        hards=jobFeatures.get("hards", "Unknown")
        softs=jobFeatures.get("softs", "Unknown")
        tools=jobFeatures.get("tools", "Unknown")
        products=jobFeatures.get("products", "Unknown")
        language=jobFeatures.get("language", "Unknown")
        
        # Redirect to the parsed job description details page
        return redirect(url_for('job_details', title=title, company=company, experience=experience, education=education, certifications=certifications, sectors=sectors, hards=hards, softs=softs, tools=tools, products=products, language=language))
    
    return render_template('parse_job.html')

@app.route('/job_details')
def job_details():
    # Get extracted resume data from query parameters
    title = request.args.get("title", "Unknown")
    company = request.args.get("company", "Not Available")
    experience = request.args.get("experience", "Not Available")
    education = request.args.get("education", "Not Available")
    sectors = request.args.get("sectors", "Not Available")
    certifications = request.args.get("certifications", "Not Available")
    hards = request.args.get("hards", "Not Available")
    softs = request.args.get("softs", "Not Available")
    tools = request.args.get("tools", "Not Available")
    products = request.args.get("products", "Not Available")
    language = request.args.get("language", "Not Available")
    
    return render_template('job_details.html', title=title, company=company, experience=experience, education=education, sectors=sectors, certifications=certifications, hards=hards, softs=softs, tools=tools, products=products, language=language)

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
            
        #flash message
        flash('Ranking successful!', 'success')

        # Redirect to results page
        return redirect(url_for('results', job_path=job_path, resumes=','.join(resume_paths)))

    return render_template('rank.html')

# Route: Results page
@app.route('/results')
def results():
    job_path = request.args.get('job_path')
    resume_paths = request.args.get('resumes').split(',')

    # Extract and process job description
    job_text = extract_text(job_path)
    #job_features = extract_job_features(job_text)
    
    job_features = exJobFeats(job_text)
    jobFeats = compJobFeats(job_features)

    ranked_resumes = []
    
    for resume_path in resume_paths:
        resume_text = extract_text(resume_path)
        #resume_features = extract_res_features(resume_text)
        
        resume_features = exResFeats(resume_text)
        resFeats = compResFeats(resume_features)

        # Calculate similarity scores
        similarity_results = calculate_similarity(jobFeats, resFeats)
        overall_similarity_score = similarity_results["overall_similarity_score"]

        ranked_resumes.append((resume_path, overall_similarity_score, similarity_results, resFeats))

    # Sort resumes by overall similarity score in descending order
    ranked_resumes.sort(key=lambda x: x[1], reverse=True)

    # Extract the filenames (or identifiers) from the resumes
    resume_filenames = ','.join([r[0] for r in ranked_resumes])
    
    return render_template(
        'results.html',
        ranked_resumes=ranked_resumes,
        job_path=job_path,
        resume_filenames=resume_filenames
    )

@app.route('/view_details')
def view_details():
    job_path = request.args.get('job_path')
    resume_path = request.args.get('resume_path')

    # Get individual similarity scores
    experience_match = float(request.args.get('exp', 0.0))
    education_match = float(request.args.get('edu', 0.0))
    skill_match = float(request.args.get('skill', 0.0))
    language_match = float(request.args.get('lang', 0.0))
    similarity_score = float(request.args.get('score', 0.0))

    # Extract job details
    job_text = extract_text(job_path)
    job_features = exJobFeats(job_text)
    jobFeats = displayJobFeats(job_features)

    # Extract resume details
    resume_text = extract_text(resume_path)
    resume_features = exResFeats(resume_text)
    resFeats = displayResFeats(resume_features)

    # Use session weights if admin is logged in, otherwise use default weights
    if session.get('admin_logged_in'):
        weights = session.get('weights', {
            'experience': 0.3,
            'education': 0.2,
            'skill': 0.4,
            'language': 0.1
        })
    else:
        weights = {
            'experience': 0.3,
            'education': 0.2,
            'skill': 0.4,
            'language': 0.1
        }

    return render_template(
        'view_details.html',
        jobFeats=jobFeats,
        resFeats=resFeats,
        similarity_score=similarity_score,
        experience_match=experience_match,
        education_match=education_match,
        skill_match=skill_match,
        language_match=language_match,
        weights=weights
    )

@app.route('/aboutUs')
def aboutUs():
    return render_template('about.html')

@app.route('/customize', methods=['GET', 'POST'])
@admin_required
def customize():
    if request.method == 'POST':
        try:
            exp = float(request.form.get('experience_weight'))
            edu = float(request.form.get('education_weight'))
            skill = float(request.form.get('skill_weight'))
            lang = float(request.form.get('language_weight'))

            total = exp + edu + skill + lang
            if total == 0:
                raise ValueError("Total weight cannot be zero.")

            # Normalize weights
            session['weights'] = {
                'experience': exp / total,
                'education': edu / total,
                'skill': skill / total,
                'language': lang / total
            }
            return redirect(url_for('rank'))
        except Exception as e:
            return f"Error: {e}", 400

    current_weights = session.get('weights', {
        'experience': 0.3,
        'education': 0.2,
        'skill': 0.4,
        'language': 0.1
    })
    return render_template('customize.html', weights=current_weights)

@app.route('/download_results', methods=['POST'])
def download_results():

    # Extract data sent from the form as hidden fields
    job_path = request.form.get('job_path')
    resume_paths = request.form.get('resumes').split(',')

    job_text = extract_text(job_path)
    job_features = exJobFeats(job_text)
    jobFeats = compJobFeats(job_features)

    ranked_resumes = []

    for resume_path in resume_paths:
        resume_text = extract_text(resume_path)
        resume_features = exResFeats(resume_text)
        resFeats = compResFeats(resume_features)

        similarity_results = calculate_similarity(jobFeats, resFeats)
        overall_similarity_score = similarity_results["overall_similarity_score"]

        ranked_resumes.append((resume_path, overall_similarity_score, similarity_results, resFeats))

    # Sort ranked resumes
    ranked_resumes.sort(key=lambda x: x[1], reverse=True)

    # Render the downloadable HTML
    html = render_template('download_results.html', ranked_resumes=ranked_resumes)

    # Serve it as a downloadable HTML file
    return send_file(
        io.BytesIO(html.encode('utf-8')),
        mimetype='text/html',
        as_attachment=True,
        download_name='ranked_results.html'
    )

if __name__ == '__main__':
    app.run(debug=True)
