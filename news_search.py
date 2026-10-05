# ==========================================
# AI NEWS RESEARCH TOOL
# News Search Engine
# ==========================================

import os
from datetime import datetime,timedelta,timezone
from dotenv import load_dotenv
from newsapi import NewsApiClient

# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

NEW_API_KEY= os.getenv("NEWS_API_KEY")

# ==========================================
# VALIDATE NEWS API KEY
# ==========================================

if not NEW_API_KEY:
    raise ValueError("NEWS_API_KEY is missing."
                     "Please add your NewsAPI key to the .env file.")

# ==========================================
# INITIALIZE NEWSAPI
# ==========================================

newsapi= NewsApiClient(api_key=NEW_API_KEY)

# ==========================================
# DETERMINE DATE RANGE
# ==========================================

def get_date_range(time_sensitivity):
    """
    Determine how far back NewsAPI should reach.
    
    high -> last 7 days
    medium -> last 30 days
    low -> last 90 days
    """
    
    today= datetime.now(timezone.utc)

    if time_sensitivity== "high":
        days= 7

    elif time_sensitivity== "medium":
        days= 30

    else:
        days=90

    from_date= today-timedelta(days=days)

    return from_date.strftime("%Y-%m-%d")

# ==========================================
# SEARCH A SINGLE QUERY
# ==========================================

def search_single_query(query,time_sensitivity= "medium", page_size=10):
    """
    Search NewsAPI using one query.
    """

    from_date= get_date_range(time_sensitivity)

    # Current/status queries should prioritize publication date

    if time_sensitivity== "high":
        sort_by= "publishedAt"

    else:
        sort_by= "relevancy"

    try:
        response= newsapi.get_everything(
            q= query,
            from_param= from_date,
            language= "en",
            sort_by= sort_by,
            page_size= page_size
        )

        return response.get("articles",[]
        )

    except Exception as error:
        print(f"NewsAPI search failed for "
              f"'{query}':{error}")

        return []
    
# ==========================================
# REMOVE DUPLICATE ARTICLES
# ==========================================

def remove_duplicates(articles):
    """
    Remove duplicate articles using
    article URL or title.
    """
    
    # Store unique articles
    unique_articles= []

    # Keep track of URLs/titles already seen
    seen= set()

    # Safety check
    if not articles:
        return[]

    # Process each article
    for article in articles:
        url= (article.get("url","") or "").strip()
        title= (article.get("title","") or "").strip()
        # URL is preferred as the unique identifier
        # Title is used as fallback
        identifier= url or title

        if not identifier:
            continue
        if identifier in seen:
            continue
        seen.add(identifier)

        unique_articles.append(article)

        # Return must be AFTER the loop
        return unique_articles

# ==========================================
# CLEAN ARTICLES
# ==========================================    

def clean_articles(articles):
    """
    Standardize the article structure.

    """
    
    cleaned= []

    # Safety check
    if not articles:
        return []

    for article in articles:
        title= (article.get("title") or "").strip()
        description= (article.get("description") or "").strip()
        url= (article.get("url") or "").strip()
        source_data= article.get("source",{})

        if isinstance(source_data, dict):
            source= (source_data.get("name") or "Unknown")
        else:
            source= str(source_data)

        published_at= (article.get("publishedAt") or "")

        # Skip articles without title or URL
        if not title or not url:
            continue

        cleaned.append({"title": title,
                        "description": description,
                        "url": url,
                        "source": source,
                        "publishedAt": published_at,
                        "author": article.get("author")})
        # Return must be AFTER the loop
        return cleaned

# ==========================================
# MAIN SEARCH FUNCTION
# ==========================================

def search_news(search_queries, time_sensitivity= "medium", max_articles= 25):
    """
    Execute multiple NewsAPI searches.
    
    Parameters
    ----------
    search_queries: list
        AI-generated search queries.
    
    time_sensitivity: str
        high/ medium/ low
        
    max_articles: int
        Maximum number of final articles.
        
    Returns
    -------
    list
        Cleaned and unique news articles.
    """

    all_articles= []

    # Safety check
    if not search_queries:
        return []

    # Minimum 5 search queries

    search_queries= search_queries[:5]

    # Search each query
    for query in search_queries:
        query= str(query).strip()

        if not query:
            continue
        print(f"Searching NewsAPI: {query}")

        articles= search_single_query(query= query, time_sensitivity= time_sensitivity, page_size= 10)

        if articles:
            all_articles.extend(articles)

        # Remove duplicates
        unique_articles= remove_duplicates(all_articles)

        # Clean article structure
        cleaned_articles= clean_articles(unique_articles)

        # For current events, sort by newest first

        if time_sensitivity== "high":
            cleaned_articles.sort(key= lambda article: article.get("publishedAt",""), reverse= True)

        # Limit final article count
        cleaned_articles= (cleaned_articles[:max_articles])

        # Limit final article count
        return cleaned_articles
    
    



