# ============================================================
# BACKEND TEST
# ============================================================

from langchain_config import run_research


queries = [

    "What is happening in Japan right now?",

    "What is the latest situation in London?",

    "What is the current situation in Tokyo?",

    "What is the latest situation regarding the earthquake in Japan?",

    "What are the latest developments at Tesla?",

    "What are the latest developments in artificial intelligence?",

    "What is happening in Mumbai today?",

    "What are the latest developments in the global economy?"

]


for query in queries:

    print("\n")
    print("=" * 80)
    print("USER QUERY")
    print("=" * 80)

    print(query)


    try:

        result = run_research(query)


        print("\n")
        print("-" * 80)
        print("QUERY UNDERSTANDING")
        print("-" * 80)

        print(
            result["query_info"]
        )


        print("\n")
        print("-" * 80)
        print("SEARCH QUERIES")
        print("-" * 80)

        for search_query in result["search_queries"]:

            print(
                "-",
                search_query
            )


        print("\n")
        print("-" * 80)
        print("NUMBER OF ARTICLES")
        print("-" * 80)

        print(
            len(result["articles"])
        )


        print("\n")
        print("-" * 80)
        print("AI RESEARCH REPORT")
        print("-" * 80)

        print(
            result["summary"]
        )


    except Exception as error:

        print("\nERROR:")
        print(error)
