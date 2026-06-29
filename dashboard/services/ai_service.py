from groq import Groq
from .prompts import evaluate_prompt,roadmap_prompt,founder_report_prompt
from .lemma_service import run_lemma_agent
import json
import time
import re
import os

client = Groq(os.getenv("GROQ_API_KEY"))


#Full Generic Ai Function that returns the output of all the agents

import json

def extract_json_only(text: str):
    if not text:
        return {}

    start = text.find("{")
    if start == -1:
        return {"error": "no_json_found"}

    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1

            if depth == 0:
                json_str = text[start:i+1]

                # hardcore cleanup
                json_str = json_str.replace("\n", " ")
                json_str = json_str.replace("\t", " ")

                try:
                    return json.loads(json_str)
                except:
                    return {
                        "error": "json_parse_failed",
                        "raw_preview": json_str[:500]
                    }

    return {"error": "no_complete_json_found"}

def normalize_prob(x):
    if x is None:
        return 0
    return round(x * 100) if x <= 1 else round(x)

def get_ai_review(prompt):
    t = time.time()
    # 1. Understanding
    print("STEP 1: BEFORE UNDERSTANDING AGENT")
    understanding_data = run_lemma_agent("understanding-agent", prompt)
    print("STEP 1 OUTPUT:", understanding_data)
    print(len(understanding_data))
    print(understanding_data)

    # 2. Evaluation
    print("evaluation-agent", round(time.time() - t, 2))
    evaluation_data = run_lemma_agent("evaluation-agent",understanding_data)
    evaluation_data = extract_json_only(evaluation_data)

    print(evaluation_data)
    print(len(evaluation_data))

    # 3. Roadmap

    prompt2 = f"""
    UNDERSTANDING OUTPUT:
    {understanding_data}

    EVALUATION OUTPUT:
    {evaluation_data}
    """
    print("roadmap-agent", round(time.time() - t, 2))
    roadmap_data = run_lemma_agent("roadmap-agent", prompt2)
    roadmap_data = extract_json_only(roadmap_data)
    print("=" * 80)
    print("ROADMAP RAW:")
    print(roadmap_data)
    print("=" * 80)
    print(len(roadmap_data))

    # 4. Founder report
    prompt3 = founder_report_prompt(understanding_data,evaluation_data,roadmap_data)
    print(len(prompt3))
    print("founder-agent", round(time.time() - t, 2))
    founder_data = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt3}]
    )

    content = founder_data.choices[0].message.content
    return json.loads(content)


