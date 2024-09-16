import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader # type: ignore
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.document_loaders import WebBaseLoader # type: ignore
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
load_dotenv()



class Chain:
    def __init__(self) -> None:
        self.llm = ChatGroq(model_name="llama-3.1-70b-versatile", temperature=0, 
                            groq_api_key="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")
    
    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
                            """
                            ### SCRAPED TEXT FROM WEBSITE:
                            {page_data}
                            ### INSTRUCTION:
                            The scraped text is from the career's page of a website.
                            Your task is to extract the job postings and return them in JSON format containing the following keys:
                            `role`, `experience`, `skills` and `description`.
                            Understand that skills might sometimes be written as 'experience in ...'
                            Only return the valid JSON.
                            ### VALID JSON (NO PREAMBLE)
                            """)

        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={
            'page_data': cleaned_text
        })
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Content too big. Unable to parse jobs")
        print(res)
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
                            """
                            ### JOB DESCRIPTION:
                            {job_description}
                            ### INSTRUCTION:
                            You are Swapnil Chhatre, a final semester Computer Science graduate student from University of Southern California. 
                            You have about 1.5 years of work experience prior to beginning Masters program in Computer Science at USC. 
                            You have worked at Center for Development of Advanced Computing for over a year as a software developer and interned with Nvidia as systems software engineer for 4 months.
                            Your course work at USC includes: Web Technologies, Algorithms, Information Retrieval and Web Search Engines, Artificial Intelligence, Natural Language Processing, Deep Learning. 
                            Your job is to write a cover letter for the job mentioned above describing the capability of Swapnil in fulfilling their needs.
                            Use information of the most relevant ones project / work experience from the following description and links to showcase Swapnil's portfolio: {link_list}. If link is `Not Available` then please do not include that in the letter.
                            You may choose to include Swapnil's most relavant coursework information if it is matching the job description. Do not include all the course work unless it matches very closely to the job description. 
                            Do not provide a preamble.
                            ### EMAIL (NO PREAMBLE):
                            """
                        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke(input={
                    "job_description": str(job),
                    "link_list": links})
        return res.content
