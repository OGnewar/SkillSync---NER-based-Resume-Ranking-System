from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory, session
from werkzeug.utils import secure_filename
import os
from modules.pdf_utils import extract_text_from_pdf
from modules.feature_extract_job import job_extract_features
from modules.feature_extract_res import res_extract_features
from modules.extract_job_features import extract_job_features
from modules.extract_res_features import extract_res_features
from modules.similarity.similarity import calculate_similarity
from modules.preprocess_text import preprocess_text

from modules.features.exResFeats import exResFeats
from modules.features.exJobFeats import exJobFeats
from modules.features.displayResFeats import displayResFeats
from modules.features.displayJobFeats import displayJobFeats
from modules.features.compJobFeats import compJobFeats
from modules.features.compResFeats import compResFeats

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"

# Configurations
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route to SkillSync Page
@app.route('/')
def skillSync():
    return render_template('skillsync.html')

# Route to Intro Page
@app.route('/intro')
def intro():
    return render_template('intro.html')

# Resume Parse Page
@app.route('/parse_res', methods=['GET', 'POST'])
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
    job_text = extract_text_from_pdf(job_path)
    #job_features = extract_job_features(job_text)
    
    job_features = exJobFeats(job_text)
    jobFeats = compJobFeats(job_features)

    ranked_resumes = []
    
    for resume_path in resume_paths:
        resume_text = extract_text_from_pdf(resume_path)
        #resume_features = extract_res_features(resume_text)
        
        resume_features = exResFeats(resume_text)
        resFeats = compResFeats(resume_features)

        # Calculate similarity scores
        similarity_results = calculate_similarity(jobFeats, resFeats)
        overall_similarity_score = similarity_results["overall_similarity_score"]

        ranked_resumes.append((resume_path, overall_similarity_score, similarity_results, resFeats))

    # Sort resumes by overall similarity score in descending order
    ranked_resumes.sort(key=lambda x: x[1], reverse=True)

    return render_template('results.html', ranked_resumes=ranked_resumes, job_path=job_path)

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
    job_text = extract_text_from_pdf(job_path)
    job_features = exJobFeats(job_text)
    jobFeats = displayJobFeats(job_features)

    # Extract resume details
    resume_text = extract_text_from_pdf(resume_path)
    resume_features = exResFeats(resume_text)
    resFeats = displayResFeats(resume_features)

    return render_template(
        'view_details.html',
        jobFeats=jobFeats,
        resFeats=resFeats,
        similarity_score=similarity_score,
        experience_match=experience_match,
        education_match=education_match,
        skill_match=skill_match,
        language_match=language_match
    )

@app.route('/aboutUs')
def aboutUs():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
