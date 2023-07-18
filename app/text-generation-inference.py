"""HuggingFace text-generation-inference backend implementation."""

import chat
from app.prompt import get_prompt
from config import settings
from text_generation import Client


def format_prompt(instruction):
    """Format the prompt for instruct text generation."""
    template = "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n###Instruction\n{instruction}\n\n### Response\n"  # noqa
    return template.format(instruction=instruction)


class Chat(chat.Chat):
    """Chatbot class implemented using MosaicML MPT"""

    def __init__(self, stream_container):
        self.stream_container = stream_container

        self.client = Client(settings.MODEL)

    def __call__(self, question, docsearch):
        """Ask a question to the chatbot."""
        prompt = get_prompt(question, docsearch)

        response = ""
        for stream in self.client.generate_stream(prompt, max_new_tokens=1024):
            if not stream.token.special:
                response += stream.token.text
            self.stream_container.markdown(response)

        self.log(question, response, prompt)
