from typing import Any

import openai
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage


class Chat:
    def __init__(self, stream_container):
        self.response = ""

        class StreamingStreamlitOutCallbackHandler(StreamingStdOutCallbackHandler):
            chat = self
            def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
                """Run on new LLM token. Only available when streaming is enabled."""
                self.chat.response += token
                stream_container.markdown(self.chat.response)

        self.chat = ChatOpenAI(
            model_name="gpt-4",
            temperature=0,
            openai_api_key=openai.api_key,
            streaming=True,
            callbacks=[StreamingStreamlitOutCallbackHandler()],
        )

    def __call__(self, question, docsearch):
        """Ask a question to the chatbot."""
        documents = docsearch.similarity_search(question, top_k=3)[:-1]
        document = "\n\n".join([doc.page_content for doc in documents])
        messages = [
            SystemMessage(
                content="You are a helpful assistant that answers questions. If unsure say 'I don't know'."
            ),
            HumanMessage(
                content=f'Given following document, please answer following question: "{question}"? '
                f'\n\nDOCUMENT: ```{document}```\n\nEND OF DOCUMENT\n\nQUESTION: "{question}"\n\n'
            ),
        ]
        print(messages[1].content)
        return self.chat(messages)
