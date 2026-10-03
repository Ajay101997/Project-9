# ============================================================
# AI NEWS RESEARCH TOOL
# Research Engine
# ============================================================

import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate


# ------------------------------------------------------------
# Load environment variables
# ------------------------------------------------------------

load_dotenv()

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)


# ------------------------------------------------------------
# Validate API key
# ------------------------------------------------------------

if not GROQ_API_KEY:

    raise ValueError(
        "GROQ_API_KEY is missing."
    )


# ------------------------------------------------------------
# Initialize Groq
# ------------------------------------------------------------

llm = ChatGroq(
    api_key=GROQ_API_KEY,

    # Current Groq model.
    model="openai/gpt-oss-120b",

    # Low temperature for factual,
    # consistent research responses.
    temperature=0.1
)


# ------------------------------------------------------------
# Research prompt
# ------------------------------------------------------------

RESEARCH_TEMPLATE = """
You are an AI news research assistant.

Your task is to analyze the retrieved news articles
and answer the user's research question.

USER QUESTION:
{query}

INTERPRETED TOPIC:
{topic}

LOCATION:
{location}

INTENT:
{intent}

RETRIEVED NEWS:
{articles}

Produce a clear research report using this structure:

## 1. Direct Answer

Answer the user's question directly based only
on the retrieved articles.

## 2. Latest Developments

Explain the most recent developments.

## 3. Important Details

Mention important facts, organizations,
companies, people, places, events or numbers
that are supported by the articles.

## 4. Location / Topic Context

Explain relevant context for the requested
location or topic.

## 5. Different Reports or Views

If different sources report different information,
clearly distinguish them.

Do not artificially create disagreement if
the sources agree.

## 6. What Is Still Unclear

Mention information that cannot be confirmed
from the retrieved articles.

## 7. Sources

List the source name and article title.

IMPORTANT RULES:

- Use only the supplied articles.
- Do not invent facts.
- Do not create unsupported numbers.
- Do not pretend that missing information is known.
- Clearly distinguish reported facts from uncertainty.
- Prioritize newer articles for current-status questions.
- Keep the answer professional and easy to understand.
"""


# ------------------------------------------------------------
# Create prompt
# ------------------------------------------------------------

research_prompt = PromptTemplate.from_template(
    RESEARCH_TEMPLATE
)


# ------------------------------------------------------------
# Create LangChain pipeline
# ------------------------------------------------------------

research_chain = research_prompt | llm


# ------------------------------------------------------------
# Prepare article information
# ------------------------------------------------------------

def prepare_articles_for_ai(
    articles
):
    """
    Convert article dictionaries into a
    readable text format for the LLM.
    """

    article_text = ""

    for index, article in enumerate(
        articles,
        start=1
    ):

        article_text += f"""
ARTICLE {index}

Title:
{article.get("title", "Unknown")}

Source:
{article.get("source", "Unknown")}

Published:
{article.get("publishedAt", "Unknown")}

Description:
{article.get("description", "No description available")}

URL:
{article.get("url", "")}

----------------------------------------
"""

    return article_text


# ------------------------------------------------------------
# Generate research report
# ------------------------------------------------------------

def generate_research_report(
    user_query,
    query_info,
    articles
):
    """
    Generate an AI-powered research report.
    """

    if not articles:

        return (
            "No sufficiently relevant news articles "
            "were found for this query."
        )

    article_text = (
        prepare_articles_for_ai(
            articles
        )
    )

    response = research_chain.invoke({

        "query": user_query,

        "topic": query_info.get(
            "topic",
            ""
        ),

        "location": query_info.get(
            "location",
            "Not specified"
        ),

        "intent": query_info.get(
            "intent",
            "general_news"
        ),

        "articles": article_text
    })

    return response.content
