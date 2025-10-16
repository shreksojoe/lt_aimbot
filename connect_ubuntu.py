import requests

r = requests.post(
        "http://192.168.1.128:11434/api/generate",
        json={"model":"gemma2:2b", "prompt":"Extract CSV fields from text: ..."}
        )

print(r.json()["response"])
