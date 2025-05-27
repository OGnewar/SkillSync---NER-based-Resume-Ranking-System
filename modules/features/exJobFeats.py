from modules.features.exMnths import extract_months

from modules.validity.validNames import validateNames
from modules.validity.validTitles import validateTitles
from modules.validity.validEmails import validateEmails
from modules.validity.validLinks import validateLinks
from modules.validity.validPhones import validatePhones
from modules.validity.validDOB import validateDOB
from modules.validity.validExpRoles import validateExpRoles
from modules.validity.validYears import validateYears
from modules.validity.validExpFields import validateExpFields
from modules.validity.validEduDeg import validateEduDeg
from modules.validity.validEduFields import validateEduFields
from modules.validity.validTerms import validateTerms

from modules.features.standardTerms import standardizeTerms

import spacy

# Load SpaCy NER model
job_spacy_model_path = "./assets/JD_Model/output/model-best"
job_ner_model = spacy.load(job_spacy_model_path)

def remove_duplicates(lst):
    return list(dict.fromkeys(lst))

def exJobFeats (text):
    
    doc = job_ner_model(text)
    
    title = validateTitles([ent.text for ent in doc.ents if ent.label_ == "JOB_TITLE"])
    company = validateNames([ent.text for ent in doc.ents if ent.label_ == "COMPANY_NAME"])
    #print(f"Job Title: {title}")
    #print(f"Company Name: {company}")
    
    expRoles = validateTerms([ent.text for ent in doc.ents if ent.label_ == "EXP_ROLE"])
    expYrs = validateYears([ent.text for ent in doc.ents if ent.label_ == "EXP_YRS"])
    expMonths = extract_months(expYrs)
    totalExpMonths = sum(int(month.split()[0]) for month in expMonths)  # Summing all months
    #totalMonths = f"{totalExpMonths} months"
    expField = validateTerms([ent.text for ent in doc.ents if ent.label_ == "EXP_FIELD"])
    expField = standardizeTerms(expField, "expFields")
    expFields = remove_duplicates(expField)
    #print(f"Exp Role: {expRoles}")
    #print(f"Exp Yrs: {expYrs}")
    #print(f"Exp Months: {expMonths}")
    #print(f"Total Months: {totalExpMonths}")
    #print(f"Exp Field: {expFields}")
    
    eduDeg = validateTerms([ent.text for ent in doc.ents if ent.label_ == "EDU_DEGREE"])
    eduDegs = standardizeTerms(eduDeg, "eduDegs")
    eduDegs = remove_duplicates(eduDegs)
    eduField = validateEduFields([ent.text for ent in doc.ents if ent.label_ == "EDU_FIELD"])
    eduFields = remove_duplicates(eduField)
    #print(f"Edu Degrees: {eduDegs}")
    #print(f"Edu Fields: {eduFields}")
    
    hard = validateTerms([ent.text for ent in doc.ents if ent.label_ == "HARD_SKILLS"])
    hards = standardizeTerms(hard, "hards")
    hards = remove_duplicates(hards)
    #print(f"Hard Skills: {hards}")
    
    soft = validateTerms([ent.text for ent in doc.ents if ent.label_ == "SOFT_SKILLS"])
    soft = standardizeTerms(soft, "soft")
    softs = remove_duplicates(soft)
    #print(f"Soft Skills: {softs}")
    
    tool = validateTerms([ent.text for ent in doc.ents if ent.label_ == "TOOLS"])
    tools = standardizeTerms(tool, "tools")
    tools = remove_duplicates(tools)
    #print(f"Tools: {tools}")
    
    product = validateTerms([ent.text for ent in doc.ents if ent.label_ == "PROD"])
    products = standardizeTerms(product, "products")
    products = remove_duplicates(products)
    #print(f"Products: {products}")
    
    sector = validateTerms({ent.text for ent in doc.ents if ent.label_ == "SECTOR"})
    sectors = remove_duplicates(sector)
    #print(f"Sector: {sectors}")
    
    certifications = validateTerms({ent.text for ent in doc.ents if ent.label_ == "CERTIFICATION"})
    #print(f"Certification: {certifications}")
    
    lang = validateTerms([ent.text for ent in doc.ents if ent.label_ == "LANGUAGE"])
    langs = standardizeTerms(lang, "langs")
    langProf = validateTerms([ent.text for ent in doc.ents if ent.label_ == "LANG_PROF"])
    langProfs = standardizeTerms(langProf, "langProfs")
    #print(f"Languages: {langs}")
    #print(f"Language Proficiency: {langProfs}")
    
    return title, company, expRoles, totalExpMonths, expFields, eduDegs, eduFields, hards, softs, tools, products, sectors, langs, langProfs, certifications, expYrs, expMonths
