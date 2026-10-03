# =========================================
# AI NEWS RESEARCH TOOL
# Streamlit Application
# =========================================

# =========================================
# 1. IMPORT LIBRARIES
# =========================================

# Import Streamlit for creating the web application
import streamlit as st

# Import the backend function that retrieves news and generates the AI research summary
from langchain_config import run_research

# =========================================
# 2. PAGE CONFIGURATION
# =========================================

# Configure the Streamlit page
st.set_page_config(page_title= "AI News Research Tool",page_icon= "📰",layout= "wide")

# =========================================
# 3. APPLICATION TITLE
# =========================================

# Display the main application title
st.title("AI News Research Tool")

# Display a short description
st.write(
    "Ask any natural-language news research question. "
    "The system analyzes your question, searches multiple "
    "news queries and generates an AI-powered research report."
)

# =========================================
# 4. SIDEBAR
# =========================================

with st.sidebar:

    st.header("Example Queries")

    st.write(
        "Try questions such as:"
    )

    st.write(
        "What is happening in Japan right now?"
    )

    st.write(
        "What is the latest situation in London?"
    )

    st.write(
        "What are the latest developments at Tesla?"
    )

    st.write(
        "What are the latest developments in AI?"
    )

    st.write(
        "What is the latest situation regarding the earthquake in Japan?"
    )

    st.write(
        "What is the latest situation regarding the earthquake in Japan?"
    )

# =========================================
# 5. USER INPUT
# =========================================

# Create a text input box for the research topic
query=st.text_area("Enter your research topic",
                   placeholder=(
                       "Example: What is happening in Japan right now"),height= 100)

# =========================================
# 6.SEARCH BUTTON
# =========================================

# Create the search button
if st.button("Get News Summary",
             type= "primary"
):
    # Check whether the user entered a query
    if not query.strip():
        # Display warning if query is empty
        st.warning("Please enter a research question")

    else:
        # Display a loading message while NewsAPI and Groq process the request
        with st.spinner("Analyzing query, searching news and generating report..."
        ):
            try:    
                # Retrieve news articles and generate the AI research summary
                result = run_research(query.strip())

            except Exception as error:
                st.error(
                    f"An error occurred:{error}"
                )

                st.stop()

        st.subheader(
            "🔎 Query Understanding"
        )

        query_info = result.get(
            "query_info",
            {}
        )


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Topic",
                query_info.get(
                    "topic",
                    "Unknown"
                )
            )

        with col2:

            st.metric(
                "Location",
                query_info.get(
                    "location"
                ) or "Not specified"
            )


        with col3:

            st.metric(
                "Intent",
                query_info.get(
                    "intent",
                    "Unknown"
                )
            )

        with col4:

            st.metric(
                "Time Sensitivity",
                query_info.get(
                    "time_sensitivity",
                    "Unknown"
                )
            )

# =========================================
# 7.SEARCH QUERIES
# =========================================

        st.subheader(
            "🔍 Generated Search Queries"
        )

        search_queries = result.get(
            "search_queries",
            []
        )


        if search_queries:

            for index, search_query in enumerate(
                search_queries,
                start=1
            ):

                st.write(
                    f"**{index}.** {search_query}"
                )

        else:

            st.warning(
                "No search queries were generated."
            )

# =========================================
# 8. AI RESEARCH REPORT
# =========================================
        st.subheader(
            "AI Research Report"
        )

        summary = result.get(
            "summary",
            ""
        )


        if summary:

            st.markdown(summary)

        else:

            st.warning(
                "No research report was generated."
            )

# =========================================
# 9. ARTICLE STATISTICS
# =========================================
        
        articles = result.get(
            "articles",
            []
        )


        st.subheader(
            "News Results"
        )


        if articles:

            st.success(
                f"{len(articles)} relevant "
                "articles found."
            )

        else:

            st.warning(
                "No relevant articles were found "
                "for this search."
            )

# =========================================
# 10. SOURCE ARTICLES
# =========================================

        st.subheader(
            "Source Articles"
        )


        if articles:

            for index, article in enumerate(
                articles,
                start=1
            ):

                title = article.get(
                    "title",
                    "No title available"
                )

                source = article.get(
                    "source",
                    "Unknown"
                )

                published_at = article.get(
                    "publishedAt",
                    "Unknown"
                )

                description = article.get(
                    "description",
                    "No description available"
                )

                url = article.get(
                    "url",
                    ""
                )


                with st.expander(
                    f"{index}. {title}"
                ):

                    st.write(
                        f"**Source:** {source}"
                    )

                    st.write(
                        f"**Published:** {published_at}"
                    )

                    st.write(
                        f"**Description:** {description}"
                    )

                    if url:

                        st.markdown(
                            f"[Read Full Article]({url})"
                        )

        else:

            st.info(
                "No source articles are available."
            )

# =========================================
# 11. FOOTER
# =========================================

    st.divider()

    st.caption(
        "AI News Research Tool | "
        "Python + LangChain + Groq + NewsAPI + Streamlit"
        )

