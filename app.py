import streamlit as st
import requests

UPLOAD_URL = "http://127.0.0.1:8000/upload_pdf/"
QUERY_URL = "http://127.0.0.1:8000/query"

st.title("AI Chat Application with PDF Knowledge Base")

# Session state for maintaining chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Upload PDF section
st.header("Upload a PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if st.button("Upload PDF"):
    if uploaded_file:
        files = {"file": uploaded_file}
        response = requests.post(UPLOAD_URL, files=files)

        if response.status_code == 200:
            st.success(response.json().get("message"))
        else:
            st.error(f"Error uploading PDF: {response.text}")

# Chat section
st.header("Chat with AI")
user_query = st.text_input("Enter your question:")

if st.button("Submit Query"):
    if user_query:
        payload = {"query": user_query}
        
        try:
            response = requests.post(QUERY_URL, json=payload)

            if response.status_code == 200:
                answer = response.json().get("answer")
                st.session_state.chat_history.append({"user": user_query, "ai": answer})
            else:
                st.error(f"Error querying PDF: {response.text}")
        except Exception as e:
            st.error(f"Exception occurred: {str(e)}")
    else:
        st.warning("Please enter a question.")

# Display chat history
if st.session_state.chat_history:
    st.subheader("Chat History")
    for chat in st.session_state.chat_history:
        st.write(f"You: {chat['user']}")
        st.write(f"AI: {chat['ai']}")
