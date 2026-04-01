import os
from groq import Groq
from dotenv import load_dotenv
import json
import re

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def run_research_agent(text):

    prompt = f"""
You are a Research Agent.

Analyze the following content and extract:

1. Product/Topic Name
2. Key Features (list)
3. Target Audience
4. Value Proposition (main benefit)
5. Any Ambiguous or unclear statements

IMPORTANT:
Return ONLY valid JSON. No markdown. No backticks.

Format:
{{
  "product": "",
  "features": [],
  "audience": "",
  "value_proposition": "",
  "ambiguities": []
}}

CONTENT:
{text}
"""

    # API call
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    output = response.choices[0].message.content

    # 🔥 Strong cleaning (fixes most JSON errors)
    clean_output = re.sub(r"```.*?```", "", output, flags=re.DOTALL).strip()

    try:
        return json.loads(clean_output)
    except:
        return {
            "error": "Failed to parse response",
            "raw_output": clean_output
        }