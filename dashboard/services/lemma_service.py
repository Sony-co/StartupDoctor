
import requests

def call_lemma(payload):
    r = requests.post(
        "https://api.lemma.work/run",  # example
        json=payload,
        headers={"Authorization": f"Bearer {os.getenv('LEMMA_API_KEY')}"}
    )
    return r.json()

#$env:PATH = "C:\Users\Admin\.local\bin;$env:PATH"