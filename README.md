Autonomous Content Factory 🤖
Project Title

Autonomous Content Factory

The Problem

Creating high-quality marketing content such as blogs, social media threads, and emails is time-consuming, error-prone, and often lacks factual verification. Teams struggle to maintain consistency and traceability across multiple content formats.

The Solution

Autonomous Content Factory automates content creation using AI. It:

Extracts and validates product information
Filters unverified or unsafe claims
Generates three polished formats: blog (500+ words), 5-part social media thread, and marketing email

The solution ensures factual integrity, smooth storytelling, and ready-to-publish outputs with minimal manual effort.

Tech Stack
Programming Languages: Python
Frameworks: Streamlit
APIs / Third-Party Tools: Groq API
Libraries: dotenv, json, re, os, time
Setup Instructions
1. Clone the repository

git clone https://github.com/13aidaaa2005-good/autonomous-content-factory.git

cd autonomous-content-factory

2. Install dependencies

pip install -r requirements.txt

3. Configure environment variables

Create a .env file in the root directory:
GROQ_API_KEY=your_groq_api_key_here

4. Run the project locally

streamlit run app.py

5. Open the app
Visit http://localhost:8501 in your browser
Paste product or article content, click Generate, and explore the generated Blog, Thread, and Email outputs