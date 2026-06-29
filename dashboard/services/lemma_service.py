
import subprocess

def run_lemma_agent(agent, message):
    result = subprocess.run(
        ["lemma", "agent", "run", agent, message],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=180
    )

    if result.returncode != 0:
        raise Exception(result.stderr)

    return result.stdout.strip()

#$env:PATH = "C:\Users\Admin\.local\bin;$env:PATH"