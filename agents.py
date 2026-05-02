from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
import streamlit as st

# ✅ Get API key
MISTRAL_API_KEY = st.secrets["MISTRAL_API_KEY"]

# LLM
llm = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0,
    mistral_api_key=MISTRAL_API_KEY,
)


# -----------------------------
# 🔍 SEARCH (NO AGENT)
# -----------------------------
def build_search_agent():
    def run(query: str):
        return web_search.invoke(query)

    return run


# -----------------------------
# 🌐 READER (NO AGENT)
# -----------------------------
def build_reader_agent():
    def run(url: str):
        return scrape_url.invoke(url)

    return run


# -----------------------------
# ✍️ WRITER
# -----------------------------
writer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert research writer."),
        (
            "human",
            """Write a detailed report.

Topic: {topic}

Research:
{research}

Structure:
- Introduction
- Key Findings
- Conclusion
- Sources""",
        ),
    ]
)

writer_chain = writer_prompt | llm | StrOutputParser()


# -----------------------------
# 🧠 CRITIC
# -----------------------------
critic_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a strict research critic."),
        (
            "human",
            """Evaluate this report:

{report}

Format:
Score: X/10
Strengths:
- ...
Weakness:
- ...
Verdict: ...""",
        ),
    ]
)

critic_chain = critic_prompt | llm | StrOutputParser()
