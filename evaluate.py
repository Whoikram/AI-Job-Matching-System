
from matcher import match_jobs


# Sample resume
resume = """
Python developer with experience in SQL,
Machine Learning, Pandas, NumPy, Excel,
Power BI, data analysis and data visualization.
"""


# Sample job descriptions
jobs = [
    """
    Data Analyst required.
    Skills: Python, SQL, Excel, Power BI,
    data analysis and statistics.
    """,

    """
    Machine Learning Engineer required.
    Skills: Python, Machine Learning,
    TensorFlow, Deep Learning and NLP.
    """,

    """
    Frontend Developer required.
    Skills: HTML, CSS, JavaScript and React.
    """
]


# Run matching system
results = match_jobs(resume, jobs)


# Display evaluation results
print("\n========== JOB MATCHING EVALUATION ==========\n")

for rank, result in enumerate(results, start=1):

    print(f"Rank: {rank}")
    print(f"Job ID: {result['job_id']}")
    print(f"Semantic Score: {result['similarity']}%")
    print(f"Skill Match: {result['skill_match']}%")
    print(f"Combined Score: {result['final_score']}%")

    print("Matched Skills:", result["matched_skills"])
    print("Missing Skills:", result["missing_skills"])

    print("-" * 45)


# Check whether Data Analyst ranked first
if results[0]["job_id"] == 1:
    print("\nPASS: Data Analyst ranked first.")
else:
    print("\nCHECK: Data Analyst did not rank first.")
