import streamlit as st
from Agents.research_agent import search_company_info, generate_structured_summary
from Agents.usecase_generation_agent import generate_use_case
from Agents.resource_collector_agent import extract_use_cases, batch_search_datasets, format_final_output
import re
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="AI Market Research Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .stTextInput input {
            border-radius: 20px;
            padding: 10px 15px;
        }
        .stButton button {
            border-radius: 20px;
            padding: 10px 25px;
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .report-header {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        .use-case-card {
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            background-color: white;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .dataset-item {
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🔍 AI Research Assistant")
    st.markdown("""
    **How it works:**
    1. Enter a company name
    2. Our AI will research the company
    3. Generate market trends and AI use cases
    4. Find relevant datasets
    """)
    st.markdown("---")
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-title">Powered by</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-content">', unsafe_allow_html=True)
    
    # Create three columns for side-by-side logos
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("Assets/Google G Icon.svg", width=70)
    
    with col2:
        st.image("Assets/Google Ai Gemini.svg", width=100)
    
    with col3:
        st.image("Assets/Facebook Meta.svg", width=100)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main app
def main():
    st.title("🤖 AI-Powered Market Research & Use Case Generator")
    st.markdown("Discover market trends, AI opportunities, and relevant datasets for any company")
    
    # Initialize session state
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'company_name' not in st.session_state:
        st.session_state.company_name = ""
    if 'research_summary' not in st.session_state:
        st.session_state.research_summary = ""
    if 'use_cases' not in st.session_state:
        st.session_state.use_cases = ""
    if 'final_report' not in st.session_state:
        st.session_state.final_report = ""
    
    # Step 1: Company Input
    if st.session_state.current_step == 1:
        st.subheader("Enter Company Name")
        company_name = st.text_input("Which company would you like to research?", placeholder="e.g., Tesla, Amazon, Starbucks")
        
        if st.button("Begin Research", key="step1"):
            if company_name:
                st.session_state.company_name = company_name
                st.session_state.current_step = 2
                st.rerun()
            else:
                st.warning("Please enter a company name")
    
    # Step 2: Research in Progress
    elif st.session_state.current_step == 2:
        st.subheader(f"🔍 Researching {st.session_state.company_name}")
        
        # Perform research with a simple spinner
        with st.spinner(f"Gathering information about {st.session_state.company_name}..."):
            try:
                # Step 1: Search company info
                raw_info = search_company_info(st.session_state.company_name)
                
                # Step 2: Generate structured summary
                st.session_state.research_summary = generate_structured_summary(st.session_state.company_name, raw_info)
                
                # Step 3: Generate use cases
                st.session_state.use_cases = generate_use_case(st.session_state.research_summary)
                
                # Step 4: Extract and enrich use cases with datasets
                extracted_use_cases = extract_use_cases(st.session_state.use_cases)
                enriched_use_cases = batch_search_datasets(extracted_use_cases)
                st.session_state.final_report = format_final_output(enriched_use_cases)
                
                st.session_state.current_step = 3
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.session_state.current_step = 1
    
    # Step 3: Display Results
    elif st.session_state.current_step == 3:
        st.success(f"Research completed for {st.session_state.company_name}!")
        
        # Create tabs for different sections
        tab1, tab2, tab3 = st.tabs(["Company Summary", "Market Trends & Use Cases", "Full Report"])
        
        with tab1:
            st.subheader("📋 Company Summary")
            st.markdown(st.session_state.research_summary)
        
        with tab2:
            st.subheader("📈 Market Trends")
            # Extract market trends section
            trends_match = re.search(r"\*\*Market Trends\*\*:(.*?)\*\*Potential AI/ML/GenAI Use Cases\*\*:", 
                                   st.session_state.use_cases, re.DOTALL)
            if trends_match:
                trends_text = trends_match.group(1).strip()
                st.markdown(trends_text)
            else:
                st.warning("Market trends section not found")
            
            st.subheader("🤖 Potential AI Use Cases")
            # Display use cases as cards
            use_cases = extract_use_cases(st.session_state.use_cases)
            for idx, uc in enumerate(use_cases, 1):
                with st.expander(f"Use Case {idx}: {uc['title']}"):
                    st.markdown(f"**Description**: {uc['description']}")
        
        with tab3:
            st.subheader("📑 Full Research Report")
            st.markdown(st.session_state.final_report, unsafe_allow_html=True)
            
            # Download button
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Generate New Report"):
                    st.session_state.current_step = 1
                    st.rerun()
            
            with col2:
                # Create download link
                report_date = datetime.now().strftime("%Y-%m-%d")
                filename = f"{st.session_state.company_name}_AI_Research_Report_{report_date}.md"
                
                # Create a download button
                st.download_button(
                    label="Download Full Report",
                    data=st.session_state.final_report,
                    file_name=filename,
                    mime="text/markdown"
                )

if __name__ == "__main__":
    main()