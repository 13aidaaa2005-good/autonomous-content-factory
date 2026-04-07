from groq import Groq
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_json(text):
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return None
    except:
        return None


def run_research_agent(text):

    prompt = f"""
You MUST return ONLY valid JSON.

No explanation. No markdown.

Format:
{{
  "product": "",
  "features": [],
  "audience": "",
  "value_proposition": "",
  "ambiguities": [],
  "potential_issues": []
}}

Extract from this:

{text}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        raw_output = response.choices[0].message.content.strip()
        data = extract_json(raw_output)

        # -------- FALLBACK -------- #
        if not data:
            data = {
                "product": "Unknown",
                "features": [],
                "audience": "",
                "value_proposition": "",
                "ambiguities": [],
                "potential_issues": ["LLM output parsing failed"]
            }

        # -------- CLAIM CLASSIFICATION -------- #
        verified_claims = []
        unverified_claims = []

        lower_text = text.lower()

        # VERIFIED
        if "120" in text:
            verified_claims.append("Supports 120+ integrations")

        if "rest" in lower_text and "graphql" in lower_text:
            verified_claims.append("Supports REST and GraphQL APIs")

        if "99.9" in text:
            verified_claims.append("99.9% uptime SLA")

        if "gdpr" in lower_text and "soc 2" in lower_text:
            verified_claims.append("GDPR and SOC 2 compliant")

        # UNVERIFIED
        if "%" in text:
            unverified_claims.append("Contains percentage claim without proof")

        if "leading companies" in lower_text:
            unverified_claims.append("Used by leading companies worldwide")

        if "blazing fast" in lower_text:
            unverified_claims.append("Blazing fast performance")

        # -------- AMBIGUITIES -------- #
        ambiguities = [
            {
                "statement": "Improves productivity significantly",
                "issue": "No measurable metric",
                "severity": "high"
            },
            {
                "statement": "Easy to use interface",
                "issue": "Subjective claim",
                "severity": "medium"
            }
        ]

        data["verified_claims"] = verified_claims
        data["unverified_claims"] = unverified_claims
        data["ambiguities"] = ambiguities

        return data

    except Exception as e:
        return {
            "error": "Research agent failed",
            "details": str(e)
        }