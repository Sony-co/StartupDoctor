
# The Prompt For yhe Understanding Agent
def design_prompt(data, readme):
    prompt = f"""
    Repository Name: {data['name']}
    Description: {data['description']}
    Stars: {data.get('stargazers_count')}
    Language: {data['language']}
    URL: {data['url']}
    ---
    ## SOURCE (README)
    {readme}
    """
    return prompt

# Prompt for the Evaluation Agent
def evaluate_prompt(data):
    prompt = f"""
    You are an expert startup investor, founder, and product strategist.

    Analyze the startup information below.

    Startup Information:

    {data}

    Evaluate the startup honestly.

    Use the following decisions ONLY:

    BUILD
    WATCH
    PIVOT
    AVOID

    Scoring Rules:

    - market_size: How large is the potential market?
    - problem_severity: How painful is the problem?
    - competition: How easy is it to compete?
    - monetization: How likely is the startup to generate revenue?
    - execution_feasibility: Can a small team realistically build it?
    - moat: How difficult is it to copy?
    - For strengths, weaknesses, risks and opportunities:
      Return 3-5 items each.
    - startup_score should be calculated from all evaluation factors.
    - confidence must be between 0 and 100.
    - Be critical and realistic. Do not be overly optimistic.

    All scores must be from 0-100.

    If information is missing, make reasonable assumptions and lower confidence.

    Return ONLY valid JSON.

    Required JSON:

    {{
    "decision":"",
        "confidence":0,
        "one_line_reason":"",

        "scores":{{
            "market_size":0,
            "problem_severity":0,
            "competition":0,
            "monetization":0,
            "execution_feasibility":0,
            "moat":0
        }},

        "strengths":[],
        "weaknesses":[],
        "risks":[],
        "opportunities":[],
        "investor_take":"",
        "founder_take":""

        "startup_score":0
    }}
    """
    return prompt

# Prompt for the roadmap agent
def roadmap_prompt(understanding_data, evaluation_data):
    prompt = f"""
    You are an expert startup mentor, founder, and accelerator advisor.

    Based on the startup understanding and evaluation below,
    create a practical roadmap for the founder.

    Startup Understanding:

    {understanding_data}

    Startup Evaluation:

    {evaluation_data}

    Focus on:
    - Validation
    - MVP development
    - Customer acquisition
    - Growth opportunities

    The roadmap should be realistic for a small startup team.

    Return ONLY valid JSON.

    Required JSON:

    {{
        "week_1": [],
        "month_1": [],
        "month_3": [],

        "validation_tasks": [],
        "mistakes_to_avoid": [],
        "growth_opportunities": [],

        "priority": "",
        "reasoning": ""
    }}
    """
    return prompt

#Prompt fo the Founder Agent
def founder_report_prompt(
        understanding_data,
        evaluation_data,
        roadmap_data):
    prompt = f"""
    You are StartupDoctor.

    Your job is to create a final founder report.

    Startup Understanding:

    {understanding_data}

    Startup Evaluation:

    {evaluation_data}

    Startup Roadmap:

    {roadmap_data}

    Create a concise final report.

    Focus on:
    - Final decision
    - Biggest strength
    - Biggest weakness
    - Biggest risk
    - Biggest opportunity
    - Most important next action
    - Choose final decision only from AVOID,BUILD and WATCH

    Return ONLY valid JSON.

    Rules:
    -Do not recalculate startup_score.
    -Use the startup_score produced by the Evaluation Agent.
    -Be conservative when estimating success_probability.
    -Most startups should score between 30 and 70.
    -Reserve scores above 80 for startups with exceptionally strong evidence of product-market fit, traction, or defensible advantages.
    -Only give scores out of 100

    Required JSON:

    {{
        "final_decision":"",
        "confidence":0,
        "success_probability":0,
        "score_breakdown": {{
        "market_size": 0,
        "problem_severity": 0,
        "competition": 0,
        "monetization": 0,
        "execution_feasibility": 0,
        "moat": 0
    }}
        "startup_score":0,

        "one_line_verdict":"",

        "startup_name":"",
        "startup_summary":"",

        "top_strength":"",
        "top_weakness":"",
        "top_risk":"",
        "top_opportunity":"",
        "why_now":""
        "ideal_customer":""
        "competitive_edge":""
        "red_flags": []
        "biggest_unknown": ""
        "startup_type": ""

        "priority":"",
        "immediate_next_action":"",

        "founder_message":"",

        "investor_view":"",
    }}
    """
    return prompt