import requests

def completeness_llm(USER_PROMPT):
    SYSTEM_PROMPT="""
    -you are given a list having multiple dictonaries
    -first dictonary is where tablename is given of data and the remaining all are each column name with number of missing values in the respective column and also missing percentage of each column
    -seeing this give me the quality of table with its column quality in 200 words
    -donot include slash n ** like your symbol by yourself
    
    """
    try:
        response=requests.post("http://localhost:11434/api/chat", json={

        "model": "qwen2.5:3b",
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": str(USER_PROMPT)
            }
             ],
        "stream": False
            })
        result = response.json()
        print(result["message"]["content"])
        return result["message"]["content"]

        # return response
    except Exception as e:
        print("Errror during calling of llm for completeness")
        raise
