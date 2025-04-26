# Import Required Libraries
import os
from serpapi import GoogleSearch
import google.generativeai as genai
import dotenv

# Load API Keys from .env File
dotenv.load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API Client
genai.configure(api_key=GEMINI_API_KEY)

# Set generation settings for Gemini model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize Gemini Generative Model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

# Function: Search Company Info using SerpAPI
def search_company_info(company_name):
    """
    Perform Google Search to collect company-related info
    using SerpAPI.

    Args:
        company_name (str): Name of the company

    Returns:
        combined_info (str): Combined text snippets from search results
    """
    params = {
        "engine": "google",
        "q": f"{company_name} industry products key areas",
        "api_key": SERPAPI_KEY,
        "num": 10
    }
    
    # Perform the search
    search = GoogleSearch(params)
    results = search.get_dict()

    # Extract snippets from organic results
    snippets = []
    for result in results.get("organic_results", []):
        if "snippet" in result:
            snippets.append(result["snippet"])

    combined_info = "\n".join(snippets)
    return combined_info

# Function: Generate Structured Summary with Gemini
def generate_structured_summary(company_name, combined_info):
    """
    Use Gemini LLM to create a clean structured company summary.

    Args:
        company_name (str): Name of the company
        combined_info (str): Raw text data from Google Search

    Returns:
        summary (str): Structured output with required fields
    """

    # Define LLM prompt
    prompt = f"""
        You are a highly knowledgeable market research assistant.

        Given the following raw search result text about "{company_name}", extract and organize the information properly.

        Important Instructions:
        - First, analyze the provided search data carefully.
        - If any required detail is missing in the search data, you MUST use your own world knowledge and information about "{company_name}" to complete it.
        - Do not leave anything as "Not Found" unless absolutely unknown even to you.
        - Always try to provide the most accurate, best-known information based on the search text and your own memory.

        Strict Output Format:
        - **Company Name**: 
        - **Industry**: 
        - **Segment**: 
        - **Products/Services**: 
        - **Key Strategic Areas**: 

        Here is the raw data:
        \"\"\"
        {combined_info}
        \"\"\"
    """

    # Generate output
    response = model.generate_content(prompt)
    return response.text.strip()
