# AI-Powered Market Research Assistant

An intelligent pipeline that researches companies, identifies market trends, generates AI use cases, and finds relevant datasets.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Methodology](#methodology)
- [Results](#results)
- [Conclusion](#conclusion)

## Overview
This application provides a comprehensive AI-powered solution for market research analysts and business strategists. It automates the process of:
1. Company research and profile generation
2. Market trend analysis
3. AI/ML use case ideation
4. Relevant dataset discovery

## Architecture
![Image](https://github.com/user-attachments/assets/f75617eb-378f-4fb7-81f4-88674799921d)


## Features
- **Automated Company Research**: Gathers comprehensive company information
- **Trend Analysis**: Identifies 3-5 key market trends
- **AI Use Case Generation**: Suggests 3-6 practical AI/ML applications
- **Dataset Discovery**: Finds relevant datasets from Kaggle, HuggingFace, and GitHub
- **Interactive UI**: User-friendly Streamlit interface
- **Exportable Reports**: Download findings in Markdown format

## Installation

1. Clone the repository:
```bash
git clone https://github.com/katakampranav/Instarez-Assessmen.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```env
SERPAPI_KEY=your_serpapi_key
gemini_api_key=your_gemini_key
TOGETHER_AI_API_KEY=your_together_ai_key
```

## Usage
1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. In the web interface:
   - Enter a company name
   - Click "Begin Research"
   - View results in the interactive dashboard
   - Download the full report

## Methodology

### Research Agent
1. Uses SerpAPI to gather raw company information from Google search results
2. Processes results with Gemini AI to create structured company profiles
3. Key fields extracted:
   - Company Name
   - Industry
   - Segment
   - Products/Services
   - Key Strategic Areas

### Use Case Generation Agent
1. Analyzes company profile using LLaMA 3.3 model
2. Identifies 3-5 current market trends relevant to the company's sector
3. Generates 3-6 specific AI/ML use cases aligned with:
   - Company products/services
   - Industry trends
   - Strategic priorities

### Resource Collector Agent
1. Extracts use cases from generated content
2. Performs batch searches for relevant datasets using:
   - Kaggle
   - HuggingFace
   - GitHub
3. Matches datasets to specific use cases
4. Formats final report with clickable resource links

## Results
The system produces comprehensive reports containing:

1. **Company Profile**:
   - Structured overview of key company information
   - Industry context and competitive positioning

2. **Market Trends**:
   - Current industry developments
   - Emerging opportunities and challenges

3. **AI Use Cases**:
   - Practical applications of AI/ML
   - Specific problem-solution pairings
   - Implementation feasibility assessment

4. **Resources**:
   - Relevant datasets with direct links
   - Implementation references
   - Data source credibility indicators

Example output snippet:
```markdown
### Use Case: Predictive Maintenance System
**Description**: AI-powered system to predict equipment failures before they occur...

**Relevant Datasets**:
- [Industrial Equipment Sensor Data](https://kaggle.com/industrial-sensors)
- [Manufacturing Failure Records](https://huggingface.co/mfg-failures)
```

## Conclusion
This implementation demonstrates:

✔ **Effective automation** of market research workflows  
✔ **Accurate trend identification** using advanced LLMs  
✔ **Practical AI use case** generation aligned with business needs  
✔ **Resource discovery** that accelerates implementation  

The pipeline combines multiple AI services into a cohesive workflow that delivers actionable insights 10x faster than manual research methods.

**Future Enhancements**:
- Integration with business intelligence platforms
- ROI estimation for proposed use cases
- Team collaboration features
- Customizable report templates

---
**Note**: This project requires API keys for SerpAPI, Google Gemini, and Together AI. Ensure you have proper subscriptions before use.
```
