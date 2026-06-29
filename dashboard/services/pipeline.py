import time
from .github_services import *
from .prompts import design_prompt
from .ai_service import get_ai_review

def startup_doctor(url):
    t = time.time()
    owner, repo = split_url(url)
    print("split-url:", round(time.time() - t, 2))

    t = time.time()
    data = get_data(owner, repo)
    print("get_data:", round(time.time() - t, 2))

    t = time.time()
    readme = get_readme(owner, repo)
    print("get_readme:", round(time.time() - t, 2))

    t = time.time()
    prompt = design_prompt(data, readme)
    print("design_prompt:", round(time.time() - t, 2))

    t = time.time()
    output = get_ai_review(prompt)
    print("get_ai_review:", round(time.time() - t, 2))

    return output

#cfc8f2577fec134e16e209d08417b2edac3dee323322322e4bbed527497e03ce