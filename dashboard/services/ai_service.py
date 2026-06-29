from groq import Groq
from .prompts import evaluate_prompt,roadmap_prompt,founder_report_prompt
import json
import time
import re
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

#Full Generic Ai Function that returns the output of all the agents

def get_ai_review(prompt):

    # 1. Understanding Agent
    print("understanding agent")
    understanding = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}]
    )


    # 2. Evaluation Agent
    print("evaluating agent")
    prompt2 = evaluate_prompt(understanding)
    evaluation = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt2}]
    )


    # 3. Roadmap Agent
    print ("roadmap")
    prompt3 = roadmap_prompt(understanding, evaluation)
    roadmap = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt3}]
    )


    # 4. Founder Report Agent
    print ("founder")
    prompt4 = founder_report_prompt(
        understanding,
        evaluation,roadmap
    )

    founder = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt4}]
    )

    content = founder.choices[0].message.content
    return json.loads(content)






