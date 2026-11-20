
# AI-Powered Job Matching System

An AI-assisted recruitment application that analyses resumes and matches candidates with relevant job opportunities using Natural Language Processing (NLP).

## Project Overview

The application extracts text from PDF resumes and compares it against multiple job descriptions using a pretrained Sentence Transformer model.

It also performs skill extraction, skill matching and skill gap analysis.

## Features

- PDF resume upload and text extraction
- Semantic similarity using Sentence Transformers
- Automatic skill extraction
- Matched and missing skill identification
- Combined job ranking
- Interactive Streamlit dashboard
- CSV export
- Evaluation script for sample job descriptions

## Technologies Used

- Python
- Streamlit
- Sentence Transformers
- Scikit-learn
- Pandas
- NumPy
- PyPDF

## AI Matching Methodology

### 1. Semantic Similarity

The pretrained all-MiniLM-L6-v2 model converts resumes and job descriptions into numerical embeddings.

Cosine similarity measures semantic similarity between the texts.

### 2. Skill Matching

A predefined skill dictionary identifies technical skills in resumes and job descriptions.

### 3. Combined Ranking

The initial ranking formula is:

Final Score = (0.70 × Semantic Similarity) + (0.30 × Skill Match)

These weights are experimental and have not yet been validated on a large dataset.

## Project Structure

- app.py - Streamlit application
- matcher.py - AI matching and skill extraction
- evaluate.py - Sample evaluation script
- requirements.txt - Python dependencies
- .gitignore - Files excluded from Git

## Installation

Clone the repository:

git clone YOUR_GITHUB_REPOSITORY_URL

Navigate to the project:

cd Ai_Job_Matching_System

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the application:

streamlit run app.py

## Evaluation

Run the sample evaluation script:

python evaluate.py

## Current Limitations

- Skill extraction uses a predefined dictionary.
- Scanned PDFs may require OCR.
- Matching scores are not probabilities of employment.
- Ranking weights require further validation.

## Future Improvements

- Advanced NLP-based skill extraction
- Improved contextual skill recognition
- Larger evaluation datasets
- Database integration
- Cloud deployment

## Author

Ikram Ali

B.Tech Instrumentation and Control Engineering
Assam Engineering College, Guwahati
