"""Prompt generation module."""
from langchain import FAISS

from config import settings


def get_prompt(question: str, docsearch: FAISS):
    """Generate a prompt for the question."""
    if settings.TOP_K:
        documents = docsearch.similarity_search(question, k=settings.TOP_K)
        document = "\n\n".join([doc.page_content for doc in documents])
        prompt = f"""{settings.SYSTEM_PROMPT}
    DOCUMENT:
    ```
    {document}
    ```
    END OF DOCUMENT

    Please answer the following question using the information provided in the DOCUMENT. "{question}"?
    """
    else:
        prompt = f"""{settings.SYSTEM_PROMPT}\n{question}?"""

    return prompt
