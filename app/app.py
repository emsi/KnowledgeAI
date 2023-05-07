import os

import openai
import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from mpt7b import Chat

openai.api_key = os.environ["OPENAI_API_KEY"]
embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)
docsearch = FAISS.load_local("/data/docsearch.1100", embeddings)

st.title("KnowledgeAI")
user_question = st.text_input("Ask a question about document:")

# Create an empty text element and store it in a variable
with st.expander("Response:", expanded=True):
    stream_container = st.empty()


if __name__ == "__main__":

    ask_question = Chat(stream_container)

    if user_question:
        docs = ask_question(user_question, docsearch)
        print(docs)