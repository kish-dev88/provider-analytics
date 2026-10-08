import os
import json
import re
from openai import OpenAI

client = OpenAI(api_key="9RETmfrxquV1SiqLJ4bcy2bRQHvQ745D",base_url="https://api.mistral.ai/v1",)

# Example retail reviews
REVIEWS = [
    "The battery lasts all day even with heavy use.",
    "The screen is bright and clear outdoors.",
    "It feels a bit heavy in the pocket.",
    "Great value for the price.",
    "Customer support was very responsive."
]

GENERATOR_PROMPT = """
You are a helpful assistant. Summarize the following customer reviews into a concise 2–3 sentence product summary.

Reviews:
{reviews}
"""

EVALUATOR_PROMPT = """
You are an evaluator. Compare the candidate summary with the reviews.

Reviews:
{reviews}

Candidate Summary:
{candidate}

Respond ONLY in JSON format:
{{
  "issues": ["list of missing points, inaccuracies, redundancy"],
  "suggested_edits": "short text with advice"
}}
"""

OPTIMIZER_PROMPT = """
You are an optimizer. Improve the candidate summary based on the evaluator's feedback.

Candidate Summary:
{candidate}

Evaluator Feedback:
{feedback}

Return only the improved summary in 2–3 sentences.
"""

# --- JSON helper ---
def extract_json(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.S)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                return {}
        return {}

# --- Generator ---
def generate_summary():
    prompt = GENERATOR_PROMPT.format(reviews=REVIEWS)
    resp = client.chat.completions.create(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return resp.choices[0].message.content.strip()

# --- Evaluator ---
def evaluate_summary(candidate):
    prompt = EVALUATOR_PROMPT.format(reviews=REVIEWS, candidate=candidate)
    resp = client.chat.completions.create(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )
    raw_output = resp.choices[0].message.content.strip()
    parsed = extract_json(raw_output)
    return parsed, raw_output

# --- Optimizer ---
def optimize_summary(candidate, feedback):
    prompt = OPTIMIZER_PROMPT.format(candidate=candidate, feedback=feedback)
    resp = client.chat.completions.create(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return resp.choices[0].message.content.strip()

# --- Pipeline ---
def run_pipeline():
    print("=== Generator Output ===")
    candidate = generate_summary()
    print(candidate, "\n")

    print("=== Evaluator Feedback ===")
    feedback_dict, feedback_raw = evaluate_summary(candidate)
    print(feedback_dict, "\n")

    print("=== Optimized Summary ===")
    improved = optimize_summary(candidate, feedback_raw)
    print(improved, "\n")

    return improved

if __name__ == "__main__":
    final_summary = run_pipeline()
