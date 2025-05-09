from modules.features.exMnths import extract_months

from modules.validity.validNames import validateNames
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

# Load SpaCy NER model and Sentence BERT model
res_spacy_model_path = "assets/Res_Model/output/model-best"
res_ner_model = spacy.load(res_spacy_model_path)

def remove_duplicates(lst):
    return list(dict.fromkeys(lst))

def exResFeats (text):
    
    doc = res_ner_model(text)
    print("--------------------------------------")
    
    name = validateNames([ent.text for ent in doc.ents if ent.label_ == "NAME"])
    email = validateEmails([ent.text for ent in doc.ents if ent.label_ == "EMAIL"])
    links = [ent.text for ent in doc.ents if ent.label_ == "LINKEDIN"]
    phone = validatePhones([ent.text for ent in doc.ents if ent.label_ == "PHONE"])
    dob = validateDOB([ent.text for ent in doc.ents if ent.label_ == "DOB"])
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Links: {links}")
    print(f"Phone: {phone}")
    print(f"DOB: {dob}")
    
    expRoles = validateTerms([ent.text for ent in doc.ents if ent.label_ == "EXP_ROLE"])
    expYrs = validateYears([ent.text for ent in doc.ents if ent.label_ == "EXP_DURATION"])
    expMonths = extract_months(expYrs)
    totalExpMonths = sum(int(month.split()[0]) for month in expMonths)  # Summing all months
    expFields = validateTerms([ent.text for ent in doc.ents if ent.label_ == "EXP_FIELD"])
    print(f"Exp Role: {expRoles}")
    print(f"Exp Yrs: {expYrs}")
    print(f"Exp Months: {expMonths}")
    print(f"Total Months: {totalExpMonths}")
    print(f"Exp Field: {expFields}")
    
    eduDeg = validateTerms([ent.text for ent in doc.ents if ent.label_ == "EDU_DEGREE"])
    eduDegs = standardizeTerms(eduDeg, "eduDegs")
    eduFields = validateEduFields([ent.text for ent in doc.ents if ent.label_ == "EDU_FIELD"])
    print(f"Edu Degrees: {eduDegs}")
    print(f"Edu Field: {eduFields}")
    
    hard = validateTerms([ent.text for ent in doc.ents if ent.label_ == "HARD_SKILLS"])
    hards = standardizeTerms(hard, "hards")
    hards = remove_duplicates(hards)
    print(f"Hard Skills: {hards}")
    
    soft = validateTerms([ent.text for ent in doc.ents if ent.label_ == "SOFT_SKILLS"])
    soft = standardizeTerms(soft, "soft")
    softs = remove_duplicates(soft)
    print(f"Soft Skills: {softs}")
    
    tool = validateTerms([ent.text for ent in doc.ents if ent.label_ == "TOOLS"])
    tools = standardizeTerms(tool, "tools")
    tools = remove_duplicates(tools)
    print(f"Tools: {tools}")
    
    product = validateTerms([ent.text for ent in doc.ents if ent.label_ == "PROD"])
    products = standardizeTerms(product, "products")
    products = remove_duplicates(products)
    print(f"Products: {products}")
    
    sector = validateTerms({ent.text for ent in doc.ents if ent.label_ == "SECTOR"})
    sectors = remove_duplicates(sector)
    print(f"Sector: {sectors}")
    
    certifications = validateTerms({ent.text for ent in doc.ents if ent.label_ == "CERTIFICATION"})
    print(f"Certification: {certifications}")
    
    interests = validateTerms([ent.text for ent in doc.ents if ent.label_ == "INTERESTS"])
    print(f"Interests: {interests}")
    
    lang = validateTerms([ent.text for ent in doc.ents if ent.label_ == "LANG"])
    langs = standardizeTerms(lang, "langs")
    langs = remove_duplicates(langs)
    langProf = validateTerms([ent.text for ent in doc.ents if ent.label_ == "LANG_PROF"])
    langProfs = standardizeTerms(langProf, "langProfs")
    print(f"Languages: {langs}")
    print(f"Language Proficiency: {langProfs}")
    
    return name, email, links, phone, dob, expRoles, expYrs, expFields, eduDegs, eduFields, hards, softs, tools, products, sector, interests, langs, langProfs, certifications, totalExpMonths, expMonths
