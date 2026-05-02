import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import streamlit as st

# API KEY from Streamlit secrets
tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])


# -----------------------------
# 🔍 SEARCH TOOL
# -----------------------------
def web_search(query: str) -> str:
    results = tavily.search(query=query, max_results=5)

    output = []

    for r in results["results"]:
        output.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}"
        )

    return "\n\n".join(output)


# -----------------------------
# 🌐 SCRAPER TOOL
# -----------------------------
def scrape_url(url: str) -> str:
    try:
        response = requests.get(
            url,
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0"},
        )

        soup = BeautifulSoup(response.text, "html.parser")

        # remove junk
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        return soup.get_text(separator=" ", strip=True)[:3000]

    except Exception as e:
        return f"Error scraping {url}: {str(e)}"
