from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain
import re


def run_research_pipeline(topic: str):
    state = {}

    # -----------------------------
    # 🔍 Step 1: Search
    # -----------------------------
    print("Running Search...\n")
    print("=" * 50)

    search_agent = build_search_agent()

    search_query = f"""
Find recent and relevant information on the topic: {topic}.
Provide a list of URLs and a brief summary of each source.
"""

    search_result = search_agent(search_query)

    state["search_result"] = search_result
    print("\nSearch Result:\n", state["search_result"])

    # -----------------------------
    # 🌐 Step 2: Extract URLs + Scrape
    # -----------------------------
    print("\nRunning Reader...\n")
    print("=" * 50)

    reader_agent = build_reader_agent()

    # Extract URLs safely
    urls = re.findall(r"https?://[^\s]+", state["search_result"])

    scraped_data = []

    for url in urls[:3]:  # limit to 3 URLs
        print(f"\nScraping: {url}")
        try:
            content = reader_agent(url)
            scraped_data.append(content[:1500])  # 🔥 limit size (VERY IMPORTANT)
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    state["scraped_content"] = "\n\n".join(scraped_data)

    print("\nScraped Content:\n", state["scraped_content"][:800])

    # -----------------------------
    # ✍️ Step 3: Writer
    # -----------------------------
    print("\n" + "=" * 50)
    print("Writing Report...")
    print("=" * 50)

    research_combined = f"""
SEARCH RESULTS:
{state['search_result'][:1000]}

SCRAPED CONTENT:
{state['scraped_content'][:2000]}
"""

    try:
        state["report"] = writer_chain(
            {
                "topic": topic,
                "research": research_combined,
            }
        )
    except Exception as e:
        state["report"] = f"Error generating report: {str(e)}"

    print("\nFinal Report:\n", state["report"])

    # -----------------------------
    # 🧠 Step 4: Critic (OPTIONAL)
    # -----------------------------
    print("\n" + "=" * 50)
    print("Critic Reviewing...")
    print("=" * 50)

    try:
        # 🔥 You can disable this if rate limit hits
        state["feedback"] = critic_chain({"report": state["report"]})
    except Exception as e:
        state["feedback"] = "Critic skipped due to API limits."

    print("\nCritic Feedback:\n", state["feedback"])

    return state


if __name__ == "__main__":
    topic = input("\nEnter a research topic: ")
    run_research_pipeline(topic)
