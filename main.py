import streamlit as st
from utils import clean_text
import portfolio
from chains import Chain
from portfolio import Portfolio
from langchain_community.document_loaders import WebBaseLoader # type: ignore


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("Cover letter Generator")
    url_input = st.text_input("Enter the URL of the job posting: ", value="https://jobs.nike.com/job/R-37999?from=job%20search%20funnel")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            print("Entering FOR LOOP")
            for job in jobs:
                skills = job.get('skills', [])
                print("GETTING LINKS FROM PORTFOLIO")
                links = portfolio.query_links(skills)
                print("GENERATING COVER LETTER")
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)

