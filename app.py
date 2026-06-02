import streamlit as st
import requests #sends http req to fastapi backend

st.title("Ask PDF")
question = st.text_input("ask a question")

if st.button("ask"):
    if question:
        with st.spinner("thinking..."):
            response = requests.post(
                "http://127.0.0.1:8000/ask",
                json = {"text":question}
            )

#Extracts only the answer value
            st.write(response.json()["answer"])