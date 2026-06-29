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

    # 4. Founder Report Agent
    print ("founder")
    founder = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}]
    )

    content = founder.choices[0].message.content
    print (content)
    return json.loads(content)






