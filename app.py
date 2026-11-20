
import streamlit as st
import pandas as pd

from pypdf import PdfReader
from matcher import match_jobs


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Job Matcher",
    page_icon="🎯",
    layout="wide"
)


# ==========================================
# 2. CUSTOM STYLING
# ==========================================

st.markdown("""
<style>

.main-title {
    font-size: 38px;
    font-weight: bold;
}

.subtitle {
    color: gray;
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. HEADER
# ==========================================

st.title("🎯 AI-Powered Job Matching System")

st.markdown(
    "An intelligent recruitment assistant "
    "using semantic search and skill gap analysis."
)

st.divider()


# ==========================================
# 4. PDF EXTRACTION
# ==========================================

def extract_resume_text(uploaded_file):

    reader = PdfReader(uploaded_file)

    resume_text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            resume_text += page_text + "\n"

    return resume_text


# ==========================================
# 5. SIDEBAR
# ==========================================

st.sidebar.title("About the Project")

st.sidebar.write(
    """
    This application compares resumes
    against job descriptions using:

    - Sentence Transformer embeddings
    - Semantic similarity
    - Skill extraction
    - Skill gap analysis
    - Job ranking
    """
)

st.sidebar.divider()

st.sidebar.write("AI Model")

st.sidebar.code("all-MiniLM-L6-v2")

st.sidebar.write("Technology Stack")

st.sidebar.write(
    """
    Python
    Streamlit
    Sentence Transformers
    Scikit-learn
    Pandas
    PyPDF
    """
)


# ==========================================
# 6. RESUME UPLOAD
# ==========================================

st.header("1. Upload Your Resume")

uploaded_file = st.file_uploader(
    "Upload your resume in PDF format",
    type=["pdf"]
)

resume_text = ""

if uploaded_file is not None:

    try:

        resume_text = extract_resume_text(uploaded_file)

        if resume_text.strip():

            st.success("Resume uploaded successfully!")

            with st.expander("Preview Extracted Resume"):

                st.text(resume_text[:4000])

        else:

            st.warning(
                "No readable text found in this PDF."
            )

    except Exception as error:

        st.error(f"Resume extraction error: {error}")


# ==========================================
# 7. JOB DESCRIPTION INPUT
# ==========================================

st.divider()

st.header("2. Enter Job Descriptions")

number_of_jobs = st.number_input(
    "Number of jobs to compare",
    min_value=1,
    max_value=10,
    value=3
)

job_descriptions = []

for i in range(int(number_of_jobs)):

    description = st.text_area(
        f"Job Description {i + 1}",
        placeholder="Paste the job description here...",
        height=130,
        key=f"job_{i}"
    )

    job_descriptions.append(description)


# ==========================================
# 8. RUN AI MATCHING
# ==========================================

st.divider()

st.header("3. AI Job Matching")

if st.button("🚀 Analyse Resume and Match Jobs"):

    if uploaded_file is None:

        st.warning("Please upload your resume.")

    elif not resume_text.strip():

        st.warning("Resume text is empty.")

    elif not all(job.strip() for job in job_descriptions):

        st.warning("Please complete all job descriptions.")

    else:

        try:

            with st.spinner(
                "AI is analysing your resume and job descriptions..."
            ):

                results = match_jobs(
                    resume_text,
                    job_descriptions
                )

            st.success("Analysis completed successfully!")

            # ==================================
            # 9. OVERALL RESUME SKILLS
            # ==================================

            st.divider()

            st.header("📌 Skills Found in Your Resume")

            from matcher import extract_skills

            resume_skills = extract_skills(resume_text)

            if resume_skills:

                st.write(", ".join(resume_skills))

            else:

                st.info(
                    "No skills from the current skill database "
                    "were detected."
                )

            # ==================================
            # 10. JOB RECOMMENDATIONS
            # ==================================

            st.divider()

            st.header("🏆 Ranked Job Recommendations")

            for rank, result in enumerate(results, start=1):

                with st.container(border=True):

                    st.subheader(
                        f"Rank #{rank} - Job {result['job_id']}"
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.metric(
                            "Semantic Similarity",
                            f"{result['similarity']}%"
                        )

                    with col2:

                        skill_score = result["skill_match"]

                        if skill_score is not None:

                            st.metric(
                                "Skill Match",
                                f"{skill_score}%"
                            )

                        else:

                            st.metric(
                                "Skill Match",
                                "Not available"
                            )

                    with col3:

                        st.metric(
                            "Combined Score",
                            f"{result['final_score']}%"
                        )

                    st.write("**Job Description:**")

                    st.write(result["job_description"])

                    st.divider()

                    # Matched skills

                    st.write("🟢 **Matched Skills**")

                    if result["matched_skills"]:

                        st.success(
                            ", ".join(result["matched_skills"])
                        )

                    else:

                        st.info("No matching skills detected.")

                    # Missing skills

                    st.write("🔴 **Missing Skills**")

                    if result["missing_skills"]:

                        st.warning(
                            ", ".join(result["missing_skills"])
                        )

                    else:

                        st.success(
                            "No missing skills detected "
                            "from the current skill database."
                        )

            # ==================================
            # 11. RESULTS TABLE
            # ==================================

            st.divider()

            st.header("📊 Matching Summary")

            summary = []

            for rank, result in enumerate(results, start=1):

                summary.append({

                    "Rank": rank,

                    "Job ID": result["job_id"],

                    "Semantic Similarity (%)":
                        result["similarity"],

                    "Skill Match (%)":
                        result["skill_match"],

                    "Combined Score (%)":
                        result["final_score"]

                })

            df = pd.DataFrame(summary)

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            # ==================================
            # 12. CSV DOWNLOAD
            # ==================================

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="📥 Download Matching Results",
                data=csv,
                file_name="AI_Job_Matching_Results.csv",
                mime="text/csv"
            )

            st.caption(
                "Scores are experimental matching indicators, "
                "not probabilities of employment."
            )

        except Exception as error:

            st.error(f"An error occurred: {error}")


# ==========================================
# 13. FOOTER
# ==========================================

st.divider()

st.caption(
    "AI Job Matching System | "
    "Python | NLP | Sentence Transformers | Streamlit"
)
