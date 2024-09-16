# Tailored Cover Letter Generator

## Description
This project generates personalized cover letters by extracting job requirements from a job posting webpage and matching them with relevant projects from a portfolio. It uses an LLM (LLaMA) to extract skills, experience, and job expectations from the job posting. The relevant skills are then queried against a personal portfolio stored in ChromaDB, and the LLM generates a customized cover letter by combining the job requirements, project links, and personal information.

## Architecture
1. **Job Posting Analysis**: The webpage content of the job posting is extracted and cleaned to retrieve the job title, required skills, and description using LLaMA.
2. **Portfolio Matching**: The portfolio, stored in ChromaDB, is queried to find the most relevant projects based on the skills extracted from the job posting.
3. **Cover Letter Generation**: The extracted portfolio data, skills, and job description are passed to LLaMA, which generates a tailored cover letter using a predefined template.

### Components:
- **`Main.py`**: Streamlit app to enter the job posting URL, extract relevant information, and generate the cover letter.
- **`chains.py`**: Contains the logic for querying job skills and generating the cover letter using LLaMA.
- **`portfolio.py`**: Loads and manages portfolio data stored in ChromaDB.
- **`utils.py`**: Cleans the extracted job posting content.

## How to Run

1. Clone the repository:
    ```bash
    git clone <repo-link>
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Add your `.env` file with your `groq_api_key`:
    ```bash
    GOOGLE_API_KEY=<your_key>
    ```

4. Run the application using Streamlit:
    ```bash
    streamlit run Main.py
    ```

5. Enter the job posting URL to generate your custom cover letter.

## Requirements
- Streamlit
- langchain
- langchain-community
- langchain-core
- pandas
- chromadb
- llama

## License
This project is licensed under the MIT License - see the LICENSE file for details.

