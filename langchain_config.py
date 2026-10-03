# ============================================================
# AI NEWS RESEARCH TOOL
# Main Research Pipeline
# ============================================================

from query_processor import process_query
from news_search import search_news
from research_engine import generate_research_report

# ==========================================
# MAIN RESEARCH FUNCTION
# ==========================================


def run_research(user_query):

    # --------------------------------------------------------
    # Step 1: Understand the user's question
    # --------------------------------------------------------
    query_info = process_query(user_query)

    # --------------------------------------------------------
    # Step 2: Get AI-generated search queries
    # --------------------------------------------------------
    search_queries = query_info.get("search_queries", [])

    # Fallback if the AI does not generate search queries
    if not search_queries:
        search_queries = [user_query]

    # --------------------------------------------------------
    # Step 3: Search news using NewsAPI
    # --------------------------------------------------------
    articles = search_news(
        search_queries=search_queries,
        time_sensitivity=query_info.get(
            "time_sensitivity",
            "medium"
        ),
        max_articles=25
    )

    # --------------------------------------------------------
    # Step 4: Generate AI research report
    # --------------------------------------------------------
    summary = generate_research_report(
        user_query=user_query,
        query_info=query_info,
        articles=articles
    )

    # --------------------------------------------------------
    # Step 5: Return all results to Streamlit
    # --------------------------------------------------------
    return {
        "query": user_query,
        "query_info": query_info,
        "search_queries": search_queries,
        "articles": articles,
        "summary": summary
    }
