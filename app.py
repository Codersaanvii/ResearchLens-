import streamlit as st

from src.rag import build_db, get_answer

st.title("Ask PDF")
uploaded_file = st.file_uploader(
    "Upload a PDF",
    type="pdf"
)

if uploaded_file:
    st.session_state.db = build_db(uploaded_file)
    question = st.text_input("ask a question")

    if st.button("ask"):
        if "db" not in st.session_state:
                st.error("please upload a PDF")
        else:
            answer = get_answer(question,
                                st.session_state.db)
#Extracts only the answer value
            st.write("answer:",answer)