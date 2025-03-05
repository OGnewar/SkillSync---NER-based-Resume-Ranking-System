from modules.similarity.simExp import experience_similarity
from modules.similarity.simEdu import education_similarity
from modules.similarity.simSkill import skill_similarity
from modules.similarity.simLang import language_similarity

# Calculate Similarity
def calculate_similarity(job, resume):
    # Calculate similarity scores for different sections
    exp = experience_similarity(job, resume) * 100 if experience_similarity(job, resume) else 0.0
    edu = education_similarity(job, resume) * 100 if education_similarity(job, resume) else 0.0
    skill = skill_similarity(job, resume) * 100 if skill_similarity(job, resume) else 0.0
    lang = language_similarity(job, resume) * 100 if language_similarity(job, resume) else 0.0

    # Compute overall weighted score
    score = (exp * 0.3) + (edu * 0.2) + (skill * 0.4) + (lang * 0.1)
    
    # Print for debugging
    print("Experience:", exp)
    print("Education:", edu)
    print("Skill:", skill)
    print("Language:", lang)
    print("Overall Score:", score)

    # Return structured results
    return { 
        "experience_match": round(exp, 2),
        "education_match": round(edu, 2),
        "skill_match": round(skill, 2),
        "language_match": round(lang, 2),
        "overall_similarity_score": round(score, 2)
    }

    
    #return round(score,2)

