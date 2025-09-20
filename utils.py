import pdfplumber
def read_pdf(file):
    """Read text from PDF and tidy it"""
    text = ""
    with pdfplumber.open(file) as pdf:
        for p in pdf.pages:
            text += p.extract_text() or ""
    return " ".join(text.split())

def score_resume(keywords, resume_text):
    """
    Simple scoring:
    - score = % of keywords found in resume
    - verdict = High/Medium/Low
    """
    matched = [k for k in keywords if k.lower() in resume_text.lower()]
    missing = [k for k in keywords if k.lower() not in resume_text.lower()]
    score = round(len(matched)/max(1,len(keywords))*100, 2)
    if score >= 75: verdict = "High"
    elif score >= 50: verdict = "Medium"
    else: verdict = "Low"
    return score, verdict, matched, missing
