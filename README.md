Dynamic Document Query Engine

This Streamlit app, Dynamic Document Query Engine, allows users to upload and query data from various document types (CSV, Excel, PDF, and Word). The app leverages machine learning models and a query engine to interpret and extract insights based on user input.

Features
-Upload Support: Accepts CSV, Excel, PDF, and Word files for data analysis.
-Data Display: Shows a preview of uploaded tabular data files.
-Query Interface: Allows users to input natural language queries on data tables.
-Document Analysis: Supports text extraction and question answering on PDF and Word files.
-Custom Query Engine: Uses a custom Pandas-based query engine for enhanced data interaction.
-LLM Integration: Powered by the Ollama model to process user queries and extract relevant data.

Installation

Use the provided requirements.txt file to install all necessary libraries:

    pip install -r requirements.txt

Note: Ensure that Ollama is installed if it’s a custom or proprietary package. If it’s hosted on a different platform or repository, include its installation link or steps here.

Run the App:

Start the Streamlit app by running:

    streamlit run app.py



Requirements

The following libraries are required to run this application:

    Streamlit: For creating the web application.
    pandas: For data manipulation and display.
    Ollama: The language model used for natural language processing (custom or proprietary).
    llama_index: For the PandasQueryEngine component.
    pdfplumber and PyPDF2: For PDF text extraction.
    docx: For processing Word documents.
    matplotlib: For rendering visual outputs.

The full list of dependencies is in requirements.txt.
Usage

    Upload Your File: Choose a CSV, Excel, PDF, or Word document to upload.
    Data Preview: If the file is a table (CSV or Excel), a preview of the data will be shown.
    Submit Queries:
        For tables, type your query in the input box to retrieve specific data insights.
        For documents, type a question to extract specific information from the text.
    View Results: Results will display below the query input, including text, tables, and visualizations.

Error Handling

If an unsupported file type is uploaded or if there is an issue processing the file, an error message will be displayed. Be sure to upload only supported file types and check the format compatibility.
Dependencies and Configuration

    Ollama: Ensure you have access to the Ollama model if it’s not publicly available on PyPI.
    Configuration: Customize settings or model parameters as needed.
