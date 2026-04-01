import os
from groq import Groq
from dotenv import load_dotenv
import json
import re

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def run_copywriter_agent(fact_sheet):

    prompt = f"""
You are a Creative Copywriter Agent.

Using the following fact sheet, generate:

1. A 500-word Blog Post (professional tone)
2. A 5-post Social Media Thread (engaging tone)
3. A 1-paragraph Email Teaser (formal tone)

IMPORTANT:
Return ONLY valid JSON. No markdown. No backticks.

Format:
{{
  "blog": "",
  "thread": ["", "", "", "", ""],
  "email": ""
}}

FACT SHEET:
{fact_sheet}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    output = response.choices[0].message.content

    clean_output = re.sub(r"```.*?```", "", output, flags=re.DOTALL).strip()

    try:
        return json.loads(clean_output)
    except:
        return {
            "error": "Failed to parse",
            "raw_output": clean_output
        }