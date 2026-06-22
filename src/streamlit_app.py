import streamlit as st

from rag import build_db, get_answer_stream

st.title("Ask PDF")
uploaded_file = st.file_uploader(
    "Upload a PDF",
    type="pdf"
)

if uploaded_file is not None:
    if "db" not in st.session_state:
        with st.spinner("processing PDF..."):
            st.session_state.db = build_db(uploaded_file)
            st.success("PDF processed")
    question = st.text_input("ask a question")

    

    if st.button("ask"):
        if question:
            response_placeholder = st.empty()
            full_response = ""

            for chunk in get_answer_stream(question,st.session_state.db):
                full_response +=chunk
                response_placeholder.markdown(full_response)

