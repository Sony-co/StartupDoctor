from groq import Groq
from .prompts import evaluate_prompt,roadmap_prompt,founder_report_prompt
import json
import time
import re
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


#Full Generic Ai Function that returns the output of all the agents

def extract_text(response):
    return response.choices[0].message.content


def safe_json_parse(text):
    try:
        return json.loads(text)
    except:
        # fallback: extract JSON block
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return {"raw_output": text}


def get_ai_review(prompt):

    # 1. Understanding Agent
    understanding = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}]
    )
    understanding_text = extract_text(understanding)

    # 2. Evaluation Agent
    prompt2 = evaluate_prompt(understanding_text)
    evaluation = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt2}]
    )
    evaluation_text = extract_text(evaluation)

    # 3. Roadmap Agent
    prompt3 = roadmap_prompt(understanding_text, evaluation_text)
    roadmap = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt3}]
    )
    roadmap_text = extract_text(roadmap)

    # 4. Founder Report Agent
    prompt4 = founder_report_prompt(
        understanding_text,
        evaluation_text,
        roadmap_text
    )

    founder = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt4}]
    )

    final_text = extract_text(founder)

    return safe_json_parse(final_text)


