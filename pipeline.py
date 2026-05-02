from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain


def run_research_pipeline(topic: str) -> str:
    state = {}
    # Step 1: Search Agent
    print("Running Search Agent...\n ")
    print("step 1: search agent")
    print("=" * 50)
    search_agent = build_search_agent()
    search_result = search_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"Find recent and relevant information on the topic: {topic}. Provide a list of URLs and a brief summary of each source.",
                )
            ],
        }
    )
    state["search_result"] = search_result["messages"][-1].content
    print("\n search result: \n", state["search_result"])

    # step 2: reader agent
    print("=" * 50)
    print("\nRunning Reader Agent...\n ")
    print("=" * 50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"""Based on the following search result about '{topic}',
Pick the most relevant URLs and scrape the content.

Search Result:
{state['search_result'][:800]}
""",
                )
            ]
        }
    )

    state["scraped_content"] = reader_result["messages"][-1].content

    print("\n scraped content: \n", state["scraped_content"])

    # step 3: writer chain

    print("\n" + "=" * 50)
    print("Step 3 - Writer is drafting the report...")
    print("=" * 50)

    research_combined = f"SEARCH RESULTS:\n{state['search_result']}\n\nSCRAPED CONTENT:\n{state['scraped_content']}"

    state["report"] = writer_chain.invoke(
        {
            "topic": topic,
            "research": research_combined,
            "info": "Write a detailed, structured research report with headings, insights, and conclusions.",
        }
    )

    print("\n Final Report: \n", state["report"])

    # critic report
    print("\n" + "=" * 50)
    print("Step 4 - Critic is reviewing the report...")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({"report": state["report"]})

    print("\n Critic Feedback: \n", state["feedback"])

    return state


if __name__ == "__main__":
    topic = input("\n Enter a research topic:  ")
    run_research_pipeline(topic)
