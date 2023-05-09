import importlib

import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from config import settings

embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
docsearch = FAISS.load_local(settings.DATA / settings.DATABASE, embeddings)

st.title(settings.APP_NAME)
user_question = st.text_input(settings.TAGLINE)

# Create an empty text element and store it in a variable
with st.expander("", expanded=True):
    stream_container = st.empty()


if __name__ == "__main__":
    Chat = importlib.import_module(settings.BACKEND).Chat
    ask_question = Chat(stream_container)

    if user_question:
        docs = ask_question(user_question, docsearch)