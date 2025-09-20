import streamlit as st
import pandas as pd
from utils import read_pdf, score_resume


st.title("Resume Relevance Checker 🚀")

# Upload JD PDF
jd_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])
# Upload Resume PDFs
resumes = st.file_uploader("Upload Resumes (PDF)", type=["pdf"], accept_multiple_files=True)

if st.button("Evaluate ▶️"):
    if not jd_file:
        st.error("Please upload JD first!")
        st.stop()
    if not resumes:
        st.error("Please upload at least one resume!")
        st.stop()

    # Extract text from JD
    jd_text = read_pdf(jd_file)

    # Simple keyword extraction: top 10 unique words >2 letters
    words = [w.lower() for w in jd_text.split() if len(w) > 2]
    keywords = list(dict.fromkeys(words))[:10]
    st.write("Keywords for evaluation:", ", ".join(keywords))

    results = []
    for r in resumes:
        resume_text = read_pdf(r)
        score, verdict, matched, missing = score_resume(keywords, resume_text)
        results.append({
            "Resume": r.name,
            "Score": score,
            "Verdict": verdict,
            "Matched": ", ".join(matched),
            "Missing": ", ".join(missing)
        })

    df = pd.DataFrame(results)
    st.dataframe(df)
    st.download_button("Download CSV", df.to_csv(index=False).encode(), "results.csv", "text/csv")
`

