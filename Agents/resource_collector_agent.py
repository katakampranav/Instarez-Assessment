# ========================================
# Imports
# ========================================
import os
import re
import dotenv
from serpapi import GoogleSearch

# ========================================
# Load API Keys
# ========================================
dotenv.load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# ========================================
# Function: Extract Potential Use Cases
# ========================================
def extract_use_cases(raw_input_text):
    """
    Extract the 'Potential AI/ML/GenAI Use Cases' section from the input text.

    Args:
        raw_input_text (str): Full text including Market Trends and Potential Use Cases.

    Returns:
        list: List of dictionaries containing use case title, description, and reference.
    """
    # Extract only the Potential Use Cases block
    match = re.search(r"\*\*Potential AI/ML/GenAI Use Cases\*\*:(.*?)$", raw_input_text, re.DOTALL)
    if not match:
        raise ValueError("Potential Use Cases section not found.")

    use_cases_block = match.group(1).strip()

    # Find all numbered use cases with title and description
    use_cases = []
    pattern = r"\d+\.\s\*\*(.*?)\*\*\s\-\s(.*)"
    matches = re.findall(pattern, use_cases_block)

    # Format each use case
    for title, description in matches:
        use_cases.append({
            "title": title.strip(),
            "description": description.strip(),
            "reference": (
                "\n- The potential AI/ML/GenAI use cases were generated using "
                "**LLaMA 3.3 model (Meta AI, 2025)** based on domain knowledge and trends.\n"
                "- The use cases align with the company's products, services, or strategies.\n"
                "- Datasets searched using **Google Search API (SERPAPI)** "
                "from trusted sources like Kaggle, HuggingFace, and GitHub."
            )
        })

    return use_cases

# ========================================
# Function: Batch Search Datasets
# ========================================
def batch_search_datasets(use_cases):
    """
    Perform an optimized batch search for datasets relevant to multiple use cases.

    Args:
        use_cases (list): List of use cases (title, description, reference).

    Returns:
        list: List of enriched use cases with attached datasets.
    """

    # Build a smart combined search query
    search_terms = " OR ".join([uc['title'] for uc in use_cases])
    query = f"datasets for {search_terms} site:kaggle.com OR site:huggingface.co OR site:github.com"

    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": 30  # Fetch more results for broader coverage
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    # Parse fetched datasets
    datasets = []
    for result in results.get("organic_results", []):
        title = result.get("title", "No Title")
        link = result.get("link", "No Link")
        snippet = result.get("snippet", "No Description")

        datasets.append({
            "title": title,
            "link": link,
            "snippet": snippet
        })

    # Match datasets intelligently with each use case
    enriched_use_cases = []
    for uc in use_cases:
        matched_datasets = []

        for ds in datasets:
            if any(keyword.lower() in (ds['title'] + ds['snippet']).lower()
                   for keyword in uc['title'].split()):
                matched_datasets.append(ds)

        enriched_use_cases.append({
            "Use Case Title": uc['title'],
            "Use Case Description": uc['description'],
            "Reference": uc['reference'],
            "Relevant Datasets": matched_datasets
        })

    return enriched_use_cases

# ========================================
# Function: Format Final Output (Markdown)
# ========================================
def format_final_output(enriched_use_cases):
    """
    Format the final output nicely in Markdown format with clickable dataset links.

    Args:
        enriched_use_cases (list): List of enriched use cases.

    Returns:
        str: Formatted markdown report.
    """

    final_output = ""

    for uc in enriched_use_cases:
        # Add use case title
        final_output += f"### Use Case: {uc['Use Case Title']}\n"
        
        # Add description
        final_output += f"**Description**: {uc['Use Case Description']}\n\n"
        
        # Add reference sources
        final_output += f"**Reference Source**: {uc['Reference']}\n\n"

        # Add matched datasets if available
        if uc["Relevant Datasets"]:
            final_output += "**Relevant Datasets:**\n"
            for ds in uc["Relevant Datasets"]:
                final_output += f"- [{ds['title']}]({ds['link']})\n"
        else:
            final_output += "_No relevant datasets found._\n"
        
        final_output += "\n---\n\n"

    return final_output
