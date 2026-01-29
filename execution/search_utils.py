import os
try:
    from duckduckgo_search import DDGS
except ImportError:
    DDGS = None

def perform_search(query, max_results=5):
    """
    Performs a web search using DuckDuckGo.
    Returns a list of dictionaries with 'title', 'href', and 'body'.
    """
    if not DDGS:
        return "Error: duckduckgo_search library not installed. Run 'pip install duckduckgo_search'."
    
    # German language focus for LingoAcademic
    results = []
    try:
        with DDGS() as ddgs:
            # Region 'de-de' for German results
            for r in ddgs.text(query, region='de-de', max_results=max_results):
                results.append({
                    "title": r['title'],
                    "link": r['href'],
                    "snippet": r['body']
                })
        return results
    except Exception as e:
        return f"Error performing search: {str(e)}"

def format_search_dossier(results):
    """Formats search results into a string dossier for the LLM."""
    if isinstance(results, str):
        return results # Error message
    
    dossier = "### Research Grounding Dossier (German Sources)\n\n"
    for i, res in enumerate(results):
        dossier += f"{i+1}. **{res['title']}**\n"
        dossier += f"   - Link: {res['link']}\n"
        dossier += f"   - Excerpt: {res['snippet']}\n\n"
    return dossier
