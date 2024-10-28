# ui.py
import streamlit as st
import requests

# Define API endpoints
UPLOAD_URL = "http://127.0.0.1:8000/upload_pdf/"
QUERY_URL = "http://127.0.0.1:8000/query"

st.title("AI Chat Application with PDF Knowledge Base")

# PDF Upload Section
st.header("Upload PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Upload the PDF to the backend
    files = {"uploaded_file": (uploaded_file.name, uploaded_file, "application/pdf")}
    response = requests.post(UPLOAD_URL, files=files)

    if response.status_code == 200:
        st.success("PDF uploaded successfully!")
    else:
        st.error(f"Error uploading PDF: {response.text}")

# Query Section
st.header("Ask a Question")
user_query = st.text_input("Enter your question:")

if st.button("Submit"):
    if user_query:
        response = requests.post(QUERY_URL, json={"query": user_query})

        if response.status_code == 200:
            answer = response.json().get("answer")
            st.success(f"Answer: {answer}")
        else:
            st.error(f"Error querying PDF: {response.text}")
    else:
        st.warning("Please enter a question.")
