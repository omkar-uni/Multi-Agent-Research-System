from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    """
    Search the web for the given query and return a summary of the results. Returns Titles, urls, and Snippets.
    """
    results = tavily.search(query=query, max_results=5)

    out = []

    for r in results["results"]:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )
    return "\n----\n".join(out)


@tool
def scrape_url(url: str) -> str:
    """Scrape the content of the given URL and return the text content."""
    try:
        response = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[
            :3000
        ]  # Return the first 2000 characters of text content
    except Exception as e:
        print(f"[red]Error scraping URL: {e}[/red]")
        return "Error scraping URL."


print(scrape_url.invoke("https://docs.langchain.com/oss/python/langchain/models"))
