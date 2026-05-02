import openai
import streamlit as st
from tools import web_search, scrape_url

# API KEY
openai.api_key = st.secrets["OPENAI_API_KEY"]


# -----------------------------
# 🔍 SEARCH
# -----------------------------
def build_search_agent():
    def run(query: str):
        return web_search.invoke(query)

    return run


# -----------------------------
# 🌐 READER
# -----------------------------
def build_reader_agent():
    def run(url: str):
        return scrape_url.invoke(url)

    return run


# -----------------------------
# ✍️ WRITER
# -----------------------------
def writer_chain(data):
    prompt = f"""
Write a detailed research report.

Topic: {data['topic']}

Research:
{data['research']}

Structure:
- Introduction
- Key Findings
- Conclusion
- Sources
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )

    return response["choices"][0]["message"]["content"]


# -----------------------------
# 🧠 CRITIC
# -----------------------------
def critic_chain(data):
    prompt = f"""
Evaluate this report:

{data['report']}

Format:
Score: X/10
Strengths:
- ...
Weakness:
- ...
Verdict: ...
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )

    return response["choices"][0]["message"]["content"]
