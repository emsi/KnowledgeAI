from typing import Any

import openai
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

from config import settings


class Chat:
    """Chatbot class. Implemented using OpenAI API."""

    def __init__(self, stream_container):
        self.response = ""

        class StreamingStreamlitOutCallbackHandler(StreamingStdOutCallbackHandler):
            chat = self

            def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
                """Run on new LLM token. Only available when streaming is enabled."""
                self.chat.response += token
                stream_container.markdown(self.chat.response)

        self.chat = ChatOpenAI(
            model_name=settings.GPT_MODEL,
            temperature=settings.TEMPERATURE,
            openai_api_key=openai.api_key,
            streaming=True,
            callbacks=[StreamingStreamlitOutCallbackHandler()],
        )

    def __call__(self, question, docsearch):
        """Ask a question to the chatbot."""
        if settings.TOP_K:
            # there's some kind of bug in docsearch atm and it returns
            # everything as a last element of the list, so we need to remove it
            documents = docsearch.similarity_search(question, top_k=settings.TOP_K)[:-1]
            document = "\n\n".join([doc.page_content for doc in documents])
            messages = [
                SystemMessage(content=settings.PROMPT),
                HumanMessage(
                    content=f'Given following document, please answer following question: "{question}"? '
                    f'\n\nDOCUMENT: ```{document}```\n\nEND OF DOCUMENT\n\nQUESTION: "{question}"\n\n'
                ),
            ]
        else:
            messages = [
                SystemMessage(content=settings.PROMPT),
                HumanMessage(content=question),
            ]
        return self.chat(messages)
