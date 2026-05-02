import openai
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url

# API KEY
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


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

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content


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

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content
