from google import genai
from config import GEMINI_API_KEY

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")
client = genai.Client(api_key=GEMINI_API_KEY)

def ask_gemini(prompt: str) -> str:
    try:
        response = client.models.generate_content(model = "gemini-2.5-flash", contents = prompt)
        text = response.text
        text = text.replace("**", "")
        text = text.replace("##", "")
        text = text.replace("\n", " ")
        return text.strip()
        
    except Exception as e:
        return f"Gemini Error: {str(e)}"