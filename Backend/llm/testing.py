import requests

SYSTEM_PROMPT = """
You are a helpful AI assistant.
Answer clearly and explain concepts with examples.
"""

USER_PROMPT = """
Explain what pandas DataFrame is.
"""

def testing():
    try:
        response = requests.post(
        "http://localhost:11434/api/chat",
        json={
        "model": "deepseek-r1:8b",
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": USER_PROMPT
            }
             ],
        "stream": False
            }
        )

        data = response.json()

        print(data["message"]["content"])
    except Exception as e:
        print("Error while testing llm")