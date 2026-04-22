from transformers import pipeline

# Load lightweight model
generator = pipeline("text-generation", model="distilgpt2")

def get_feedback(resume, jd):
    prompt = f"""
    You are an expert career coach.

    Give ONLY clean bullet points.

    Strict format:

    Missing Skills:
    - Python
    - Machine Learning
    - SQL

    Improvements:
    - Add projects with measurable results
    - Improve resume formatting

    Suggestions:
    - Build 2 strong ML projects
    - Practice DSA daily

    Do NOT repeat resume.
    Do NOT write paragraphs.
    Only bullet points.

    Resume:
    {resume[:1000]}

    Job Description:
    {jd}
    """

    result = generator(prompt, max_length=250, temperature=0.6)

    return result[0]["generated_text"]