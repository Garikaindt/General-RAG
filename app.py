import subprocess
import os
import streamlit as st

# Run the setup.py script
if not os.path.isfile('setup_done'):
    subprocess.run(['python', 'setup.py'])
    with open('setup_done', 'w') as f:
        f.write('setup done')

# Your existing Streamlit code
# ...

import pandas as pd
from llama_index.experimental.query_engine.pandas import PandasQueryEngine
from langchain_community.llms import Ollama
from io import BytesIO
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader
from docx import Document
import pdfplumber

# Streamlit App Layout
st.title("Dynamic Document Query Engine")

# File uploader for CSV, Excel, PDF, and Word files
uploaded_file = st.file_uploader("Upload your CSV, Excel, PDF, or Word file", type=["csv", "xlsx", "pdf", "docx"])

# Helper function to extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
    except:
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    return text

# Helper function to extract text from Word file
def extract_text_from_word(file):
    doc = Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# Helper function to create a DataFrame from Excel file
def read_excel_file(file):
    return pd.read_excel(file)

if uploaded_file is not None:
    # Determine file type and read appropriately
    file_type = uploaded_file.name.split('.')[-1]

    if file_type == 'csv':
        df = pd.read_csv(uploaded_file)
    elif file_type == 'xlsx':
        df = read_excel_file(uploaded_file)
    elif file_type == 'pdf':
        extracted_text = extract_text_from_pdf(uploaded_file)
        df = None
    elif file_type == 'docx':
        extracted_text = extract_text_from_word(uploaded_file)
        df = None
    else:
        st.error("Unsupported file format.")
        df = None

    if df is not None:
        st.subheader("Dataset Preview")
        st.dataframe(df.head())
        llm = Ollama(model="mistral")

        class CustomPandasQueryEngine(PandasQueryEngine):
            def _query(self, query_bundle):
                context = self._get_table_context()
                pandas_instructions = self._llm.invoke(
                    input=self._pandas_prompt.template.format(
                        df_str=context,
                        query_str=query_bundle.query_str,
                        instruction_str=self._instruction_str
                    )
                )
                if self._verbose:
                    st.write(f"> Pandas Instructions:\n```\n{pandas_instructions}\n```\n")
                try:
                    result = eval(pandas_instructions, {"df": self._df, "pd": pd})
                except KeyError as e:
                    result = f"Column not found: {e}"
                except Exception as e:
                    result = f"An error occurred: {e}"
                return {"response": {"result": result}}

        query_engine = CustomPandasQueryEngine(df=df, llm=llm, verbose=True)
        query = st.text_input("Enter your query:", "")
        if st.button("Submit Query"):
            if query:
                response = query_engine.query(query)
                result = response['response']['result']
                if isinstance(result, (int, float)):
                    st.write(result)
                elif isinstance(result, pd.DataFrame):
                    st.write(result)
                elif isinstance(result, plt.Axes):
                    buf = BytesIO()
                    plt.savefig(buf, format='png')
                    st.image(buf)
                    plt.close()
                else:
                    st.write(result)
            else:
                st.warning("Please enter a query.")
    else:
        # If it's not a tabular file, show extracted text
        st.subheader("Extracted Text Preview")
        st.write(extracted_text[:1000])  # Preview first 1000 characters

        if extracted_text:
            llm = Ollama(model="mistral")
            query = st.text_input("Ask a question about the document:", "")
            if st.button("Submit Query for Document"):
                if query:
                    # Send the extracted text as context to the LLM
                    response = llm.invoke(input=f"Context: {extracted_text}\n\nQuestion: {query}")
                    st.write(response)
                else:
                    st.warning("Please enter a question.")
else:
    st.info("Please upload a CSV, Excel, PDF, or Word file to get started.")
