import wolframalpha
import os
from dotenv import load_dotenv

load_dotenv()

def query_wolfram(query):
    """Queries WolframAlpha and returns the text result."""
    app_id = os.getenv("WOLFRAMALPHA_APP_ID")
    if not app_id:
        return "API key not found. Please check your .env file."
    
    try:
        client = wolframalpha.Client(app_id)
        res = client.query(query)
        answer = next(res.results).text
        return answer
    except Exception as e:
        print(f"[ERROR] WolframAlpha query failed: {e}")
        return "I couldn't find an answer for that calculation."
