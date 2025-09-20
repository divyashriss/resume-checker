# by Divyashri - Hackathon MVP
import streamlit as st
from docx import Document
import pdfplumber
from rapidfuzz import fuzz
import pandas as pd
import re
import tempfile, os
from pathlib import Path

st.title("Resume Relevance Checker 🚀")

# Upload JD
jd_file = st.file_uploader("Upload JD file (optional)", type=["pdf","docx","txt"])
jd_text = st.text_area("Or paste JD text here", height=150)

# Upload resumes
resumes = st.file_uploader("Upload resumes", type=["pdf","docx","txt"], accept_multiple_files=True)

# Simple helpers
def tidy(text):
    if not text: return ""
    text = text.replace("\n"," ").replace("\r"," ")
    return re.sub(r"\s+"," ", text).strip()

def extract_text(file):
    suffix = Path(file.name).suffix.lower()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(file.read()); tmp.close()
    text=""
    try:
        if suffix==".pdf":
            with pdfplumber.open(tmp.name) as pdf:
                text = " ".join([p.extract_text() or "" for p in pdf.pages])
        elif suffix in [".docx",".doc"]:
            doc = Document(tmp.name)
            text = " ".join([p.text for p in doc.paragraphs])
        else:
            text = tmp.read().decode("utf-8", errors="ignore")
    finally:
        try: os.unlink(tmp.name)
        except: pass
    return tidy(text)

def score_resume(keywords, resume_text, threshold=70):
    matched, missing = [], []
    for k in keywords:
        s = fuzz.partial_ratio(k.lower(), resume_text.lower())
        if s>=threshold: matched.append(k)
        else: missing.append(k)
    hard = round(len(matched)/max(1,len(keywords))*100,2)
    return hard, matched, missing

# Run evaluation
if st.button("Evaluate ▶️"):
    if jd_file: jd = extract_text(jd_file)
    else: jd = jd_text
    jd = tidy(jd)
    if not jd: st.error("Provide JD text"); st.stop()

    # simple keyword extraction (top words)
    keywords = [w for w in re.findall(r'\w+', jd.lower()) if len(w)>2][:12]
    st.write("Keywords:", ", ".join(keywords))

    if not resumes: st.error("Upload at least 1 resume"); st.stop()

    rows=[]
    for f in resumes:
        text = extract_text(f)
        hard, matched, missing = score_resume(keywords, text)
        score = hard
        if score>=75: verdict="High"
        elif score>=50: verdict="Medium"
        else: verdict="Low"
        rows.append({"file":f.name,"score":score,"verdict":verdict,"matched":", ".join(matched),"missing":", ".join(missing)})
    df = pd.DataFrame(rows)
    st.dataframe(df)
    st.download_button("Download CSV", df.to_csv(index=False).encode(), "results.csv","text/csv")
