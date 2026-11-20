
import re

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# 1. LOAD PRETRAINED AI MODEL
# ==========================================

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


# ==========================================
# 2. DEFINE SKILL DATABASE
# ==========================================


SKILL_ALIASES = {

    "Python": ["python"],

    "SQL": ["sql", "mysql", "postgresql"],

    "Machine Learning": ["machine learning", "ml"],

    "Deep Learning": ["deep learning", "dl"],

    "NLP": ["nlp", "natural language processing"],

    "TensorFlow": ["tensorflow"],

    "Scikit-learn": ["scikit-learn", "scikit learn", "sklearn"],

    "PyTorch": ["pytorch"],

    "Pandas": ["pandas"],

    "NumPy": ["numpy"],

    "Excel": ["excel", "microsoft excel"],

    "Power BI": ["power bi", "powerbi", "microsoft power bi"],

    "Tableau": ["tableau"],

    "Data Visualization": [
        "data visualization",
        "data visualisation"
    ],

    "Statistics": ["statistics", "statistical analysis"],

    "Java": ["java"],

    "C++": ["c++"],

    "FastAPI": ["fastapi"],

    "Flask": ["flask"],

    "REST API": ["rest api", "restful api", "rest apis"],

    "Git": ["git", "github"],

    "Docker": ["docker"],

    "AWS": ["aws", "amazon web services"],

    "Azure": ["azure"],

    "Streamlit": ["streamlit"],

    "Firebase": ["firebase"],

    "Arduino": ["arduino"],

    "ESP32": ["esp32"],

    "IoT": ["iot", "internet of things"],

    "Computer Vision": ["computer vision"],

    "Data Analysis": ["data analysis"],

    "Data Structures": ["data structures"],

    "OOP": [
        "object oriented programming",
        "object-oriented programming",
        "oop"
    ],

    "HTML": ["html"],

    "CSS": ["css"],

    "JavaScript": ["javascript"]

}



# ==========================================
# 3. EXTRACT SKILLS FROM TEXT
# ==========================================

def extract_skills(text):

    text = text.lower()

    detected_skills = []

    for skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(alias)
                + r"(?![a-z0-9])"
            )

            if re.search(pattern, text):

                detected_skills.append(skill)
                break

    return sorted(detected_skills)


# ==========================================
# 4. CALCULATE SKILL MATCHING
# ==========================================

def calculate_skill_match(resume_skills, job_skills):

    matched = sorted(set(resume_skills) & set(job_skills))

    missing = sorted(set(job_skills) - set(resume_skills))

    if not job_skills:
        return {
            "matched_skills": matched,
            "missing_skills": missing,
            "skill_match": None
        }

    score = (
        len(matched) / len(job_skills)
    ) * 100

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "skill_match": round(score, 2)
    }


# ==========================================
# 5. MAIN JOB MATCHING FUNCTION
# ==========================================

def match_jobs(resume_text, job_descriptions):

    if not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    if not job_descriptions:
        raise ValueError("No job descriptions provided.")

    if not all(job.strip() for job in job_descriptions):
        raise ValueError("Job descriptions cannot be empty.")

    # Extract resume skills
    resume_skills = extract_skills(resume_text)

    # Generate resume embedding
    resume_embedding = model.encode(
        [resume_text],
        normalize_embeddings=True
    )

    # Generate job embeddings
    job_embeddings = model.encode(
        job_descriptions,
        normalize_embeddings=True
    )

    # Calculate semantic similarity
    semantic_scores = cosine_similarity(
        resume_embedding,
        job_embeddings
    )[0]

    results = []

    for index, job in enumerate(job_descriptions):

        # Extract job skills
        job_skills = extract_skills(job)

        # Calculate skill matching
        skill_results = calculate_skill_match(
            resume_skills,
            job_skills
        )

        # Convert semantic similarity to percentage
        semantic_score = max(
            0,
            min(100, float(semantic_scores[index]) * 100)
        )

        # Combine scores when job skills are detected
        if skill_results["skill_match"] is not None:

            final_score = (
                0.70 * semantic_score
                + 0.30 * skill_results["skill_match"]
            )

        else:
            final_score = semantic_score

        results.append({

            "job_id": index + 1,

            "job_description": job,

            "similarity": round(semantic_score, 2),

            "skill_match": skill_results["skill_match"],

            "matched_skills": skill_results["matched_skills"],

            "missing_skills": skill_results["missing_skills"],

            "required_skills": job_skills,

            "final_score": round(final_score, 2)

        })

    # Rank using combined score
    results.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    return results
