import openai
import streamlit as st
from tools import web_search, scrape_url

# Set API key
openai.api_key = st.secrets["OPENAI_API_KEY"]


# -----------------------------
# 🔍 SEARCH AGENT
# -----------------------------
def build_search_agent():
    def run(query: str):
        return web_search(query)

    return run


# -----------------------------
# 🌐 READER AGENT
# -----------------------------
def build_reader_agent():
    def run(url: str):
        return scrape_url(url)

    return run


# -----------------------------
# ✍️ WRITER
# -----------------------------
def writer_chain(data):
    prompt = f"""
You are an expert research writer.

Topic: {data['topic']}

Research:
{data['research']}

Write a structured report with:
- Introduction
- Key Findings (at least 3 points)
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
You are a strict research critic.

Report:
{data['report']}

Respond in this format:

Score: X/10

Strengths:
- ...
- ...

Weakness:
- ...
- ...

Verdict: ...
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )

    return response["choices"][0]["message"]["content"]
