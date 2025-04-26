from together import Together
import os
import dotenv

# Load environment variables
dotenv.load_dotenv()

TOGETHER_AI_API_KEY = os.getenv("TOGETHER_AI_API_KEY")

# Initialize Together API client
client = Together(api_key=TOGETHER_AI_API_KEY)

def generate_use_case(research_summary):
    """
    Generate AI/ML/GenAI use cases based on the company research summary.

    Args:
        research_summary (str): The research summary to base the use cases on.

    Returns:
        str: The generated use cases.
    """

    prompt = f"""
        You are an expert AI strategist and market research analyst.

        Given the following company research summary, perform two tasks carefully:

        ---

        **Part 1: Identify Current Market Trends**
        - Based on the company's industry and segment, identify 3-5 important current market trends.
        - Think from a global and industry-specific perspective.
        - Use your own knowledge if necessary, not limited to only the provided text.
        - Trends must be real-world, practical, and written clearly.

        ---

        **Part 2: Generate AI/ML/GenAI Use Cases**
        - Based on the research summary and identified market trends, find potential areas where AI, ML, or GenAI solutions can help the company.
        - Suggest use-cases aligned with the company’s products, services, or key strategic areas.
        - Use your own knowledge if necessary.
        - Mention 3-6 specific use-cases.
        - Each use-case should have a short, clear one-line description.

        ---

        **Output Format (strict)**:

        - **Market Trends**:
            1. [Trend Title] - [One-line explanation]
            2. [Trend Title] - [One-line explanation]
            3. [Trend Title] - [One-line explanation]
            (At least 3 trends)

        - **Potential AI/ML/GenAI Use Cases**:
            1. [Use Case Title] - [Short one-line description]
            2. [Use Case Title] - [Short one-line description]
            3. [Use Case Title] - [Short one-line description]
            (At least 3 use-cases)

        ---

        Here is the company research summary:
        \"\"\"
        {research_summary}
        \"\"\"
    """


    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

# Example usage
if __name__ == "__main__":
    research_summary = """
    - Company Name: Tesla, Inc.
    - Industry: Automotive and Energy
    - Segment: Electric Vehicles, Energy Storage, Solar Energy
    - Products/Services: Electric Cars (Model S, Model 3, Model X, Model Y, Cybertruck), Solar Panels, Battery Energy Storage
    - Key Strategic Areas: Sustainable Energy Solutions, Autonomous Driving, Manufacturing Innovation
    """
    
    use_cases = generate_use_case(research_summary)
    print(use_cases)