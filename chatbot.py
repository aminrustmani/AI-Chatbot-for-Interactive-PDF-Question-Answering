import streamlit as st
import google.generativeai as genai
import os
import pdfplumber

# Configure Gemini API (Recommended: use env variable)
genai.configure(api_key="AIzaSyBMnh3PjAcVgin_M97qbLH2Q1fTQHrMs4U")

# Initialize model
model = genai.GenerativeModel("gemini-1.5-pro-latest")

st.set_page_config(page_title="Gemini Chatbot with PDF", page_icon="🤖")
st.title("💬Chatbot with PDF Support")

# Upload PDF
pdf = st.file_uploader("Upload a PDF", type="pdf")

pdf_text = ""
if pdf:
    try:
        with pdfplumber.open(pdf) as pdf_file:
            for page in pdf_file.pages:
                text = page.extract_text()
                if text:
                    pdf_text += text + "\n"
        st.success("PDF uploaded and processed successfully!")
    except Exception as e:
        st.error(f"Failed to read PDF: {str(e)}")

# Chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input
prompt = st.chat_input("Ask something...")

if prompt:
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        with st.spinner("Thinking..."):
            if pdf_text:
                full_prompt = f"""You are a helpful assistant. Answer the question based on the following PDF content:\n\n{pdf_text}\n\nQuestion: {prompt}"""
            else:
                full_prompt = prompt

            response = model.generate_content(full_prompt)
            reply = response.text
    except Exception as e:
        reply = f"Error: {str(e)}"

    # Show Gemini reply
    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
