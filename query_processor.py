# ==========================================
# AI NEWS RESEARCH TOOL
# Query Processor
# ==========================================

# Convert a natural-language user question into structured information that can be used to search news effectively
import os
import json

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

# Import environment variables from the .env file
load_dotenv()

# Retrieve the Groq API key
GROQ_API_KEY= os.getenv("GROQ_API_KEY")

# ==========================================
# VALIDATE API KEYS
# ==========================================

# Check whether the Groq API key is available
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing."
                     "Please add it to the .env file.")

# ==========================================
# INITIALIZE GROQ MODEL
# ==========================================

llm=ChatGroq(api_key=GROQ_API_KEY,
             # Current Groq production model suitable for research and structered outputs
             model="openai/gpt-oss-120b",
             # Lower temperature gives more consistent results
             temperature=0.1)

# ==========================================
# QUERY ANALYSIS PROMPT
# ==========================================
QUERY_ANALYSIS_TEMPLATE= """
You are an intelligent news research query analyzer.

Analyze the user's natural-language question.

The application must work for ANY:

- country
- state
- city
- district
- town
- organization
- company
- person
- event
- technology
- sport
- business topic
- economic topic
- political topic
- disaster
- weather event
- scientific topic
- general news topic

Do NOT assume a particular location.

Do NOT hard-code locations.

Do NOT answer the user's question.

Do NOT invent facts.

USER QUESTION:
{query}

Return ONLY valid JSON.

Required JSON fields:

topic
location
intent
time_sensitivity
keywords
search_queries

Definitions:

topic:
The main subject of the question.

location:
The location mentioned in the question.
If there is no location, use null.

entities:
Important people, companies, organizations,
locations, events or other entities.

intent:
Choose one:
current_status
latest_news
general_news
background
event_update
business_update
disaster_update
sports_update
technology_update
other

time_sensitivity:
Choose one:
high
medium
low

keywords:
Important keywords from the question.

search_queries:
Generate 3 to 5 different search queries
that can be sent to a news API.


Rules:

1. Preserve important names and locations.

2. If the questions contains words such as:
current
today
latest
now
status
situation
recent
update
happening 
right now

then time_sensitivity should normally be high.

3. If location is mentioned,
include that location in relevant search queries.

4. If no location is mentioned,
do not invent one.

5. For disasters, accidents, conflicts,
weather events, elections, company events,
sports events and other developing situations,
prioritize recent news.

6. Search queries should be short and useful
for a news search API.

7. Generate multiple variations.

8. Do not answer the user's question.

9. Return JSON only.

Example:
{{
    "topic": "current situation",
    "location": "Japan",
    "entities": ["Japan"],
    "intent": "current_status",
    "time_sensitivity": "high",
    "keywords": ["Japan", "current", "situation"],
    "search_queries": [
        "Japan latest news",
        "Japan current situation",
        "Japan latest developments",
        "Japan news today"
    ]
}}
"""

# ==========================================
# CREATE LANGCHAIN PROMPT
# ==========================================

prompt= PromptTemplate(
    template=QUERY_ANALYSIS_TEMPLATE,
    input_variables=["query"])

# ==========================================
# CREATE LANGCHAIN PIPELINE
# ==========================================

query_chain= prompt|llm

# ==========================================
# HELPER FUNCTION TO CLEAN JSON OUTPUT
# ==========================================

def clean_json_response(response_text):

    text= response_text.strip()

    if text.startswith("```json"):
        text= text[7:]

    elif text.startswith("```"):
        text= text[3:]

    if text.endswith("```"):
        text= text[:-3]

    return text.strip()

# ==========================================
# CREATE FALLBACK SEARCH QUERIES
# ==========================================

def create_fallback_queries(user_query):

    query = user_query.strip()

    if not query:
        return []

    queries = [
        query,
        f"{query} latest news",
        f"{query} latest developments",
        f"{query} today"
    ]

    # Remove duplicates while preserving order
    unique_queries = []

    for item in queries:

        item = item.strip()

        if item and item not in unique_queries:
            unique_queries.append(item)

    return unique_queries[:5]

# ==========================================
# MAIN QUERY PROCESSING FUNCTION
# ==========================================

def process_query(user_query):

    # Remove unnecessary whitespace
    user_query= user_query.strip()

    # Validate user input
    if not user_query:
        return{"topic": "",
            "location": None,
            "entities": [],
            "intent": "other",
            "time_sensitivity": "medium",
            "keywords": [],
            "search_queries": []
            }
    # Send the question to Groq

    try:

        response = query_chain.invoke({
            "query": user_query
        })

        response_text = clean_json_response(
            response.content
        )

        result = json.loads(response_text)

    except Exception as error:

        print(
            f"Query analysis failed: {error}"
        )

        # Even if Groq fails, the application continues
        result = {
            "topic": user_query,
            "location": None,
            "entities": [],
            "intent": "general_news",
            "time_sensitivity": "high",
            "keywords": user_query.split(),
            "search_queries": []
        }

# ==========================================
# VALIDATE REQUIRED FIELDS
# ==========================================

    if not isinstance(result, dict):

        result = {}

    topic = result.get("topic") or user_query

    location = result.get("location")

    entities = result.get("entities", [])

    intent = result.get(
        "intent",
        "general_news"
    )

    time_sensitivity = result.get(
        "time_sensitivity",
        "medium"
    )

    keywords = result.get(
        "keywords",
        []
    )

    search_queries = result.get(
        "search_queries",
        []
    )

# ==========================================
# MAKE SURE LISTS ARE ACTUALLY LISTS
# ==========================================

    if not isinstance(entities, list):
        entities = [str(entities)]

    if not isinstance(keywords, list):
        keywords = [str(keywords)]

    if not isinstance(search_queries, list):
        search_queries = []

# ==========================================
# REMOVE EMPTY SEARCH QUERIES
# ==========================================

    search_queries = [
        str(q).strip()
        for q in search_queries
        if str(q).strip()
    ]

# ==========================================
# CRITICAL FALLBACK
# ==========================================

# If Groq did not generate usable search queries,
# create them automatically from the original question.

    if not search_queries:

        search_queries = create_fallback_queries(
            user_query
        )

# ==========================================
# REMOVE DUPLICATE QUERIES
# ==========================================

    final_queries = []

    for query in search_queries:

        if query not in final_queries:
            final_queries.append(query)

# ==========================================
# LIMIT TO MAXIMUM 5 QUERIES
# ==========================================

    final_queries = final_queries[:5]

# ==========================================
# RETURN STANDARDIZED RESULT
# ==========================================

    return {
        "topic": topic,
        "location": location,
        "entities": entities,
        "intent": intent,
        "time_sensitivity": time_sensitivity,
        "keywords": keywords,
        "search_queries": final_queries
    }

