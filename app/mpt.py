"""MosaicML MPT backend implementation."""
import streamlit as st
import torch
import transformers

import chat
from config import settings


# Define a function to load the large language model
@st.cache_resource(show_spinner=f"Please wait. Loading {settings.MODEL}...")
def load_large_language_model_pipeline(
    model_name,
    *,
    torch_dtype=None,
    trust_remote_code=None,
    use_auth_token=None,
    padding_side="left",
    task="text-generation",
    device=None,
    streamer=None,
):
    """Load the large language model and tokenizer."""

    config = transformers.AutoConfig.from_pretrained(model_name, trust_remote_code=True)
    # config.attn_config['attn_impl'] = 'triton'  # change this to use triton-based FlashAttention
    device = device or torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    config.init_device = device

    model = transformers.AutoModelForCausalLM.from_pretrained(
        model_name,
        config=config,
        torch_dtype=torch_dtype,
        trust_remote_code=trust_remote_code,
        use_auth_token=use_auth_token,
        # low_cpu_mem_usage=True,
    )
    tokenizer = transformers.AutoTokenizer.from_pretrained(
        model_name,
        trust_remote_code=trust_remote_code,
        use_auth_token=use_auth_token,
        padding_side=padding_side,
    )
    # model.to(device=device, dtype=torch.bfloat16)

    if streamer is None:
        streamer = transformers.TextStreamer(
            tokenizer,
            skip_prompt=True,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
        )
    else:
        streamer = streamer(
            tokenizer,
            skip_prompt=True,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
        )

    return transformers.pipeline(
        task,
        model=model,
        tokenizer=tokenizer,
        device=device,
        streamer=streamer,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id,
    )


def format_prompt(instruction):
    """Format the prompt for instruct text generation."""
    template = "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n###Instruction\n{instruction}\n\n### Response\n"  # noqa
    return template.format(instruction=instruction)


class Chat(chat.Chat):
    """Chatbot class implemented using MosaicML MPT"""

    def __init__(self, stream_container):
        self.response = ""
        self.stream_container = stream_container

        class StreamlitTextStreamer(transformers.TextStreamer):
            chat = self

            def on_finalized_text(self, text: str, stream_end: bool = False):
                """Run on finalized text. Only available when streaming is enabled."""
                self.chat.response += text
                if stream_end:
                    self.chat.response += "\n"
                stream_container.markdown(self.chat.response)

        # Initialize the model and tokenizer
        self.pipeline = load_large_language_model_pipeline(
            settings.MODEL,
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
            streamer=StreamlitTextStreamer,
        )

    def __call__(self, question, docsearch):
        """Ask a question to the chatbot."""
        if settings.TOP_K:
            documents = docsearch.similarity_search(question, k=settings.TOP_K)
            document = "\n\n".join([doc.page_content for doc in documents])
            prompt = f"""{settings.SYSTEM_PROMPT}

Given following document, please answer following question: "{question}"?

DOCUMENT:
```
{document}
```

END OF DOCUMENT

QUESTION: "{question}"?
"""
        else:
            prompt = f"""{settings.SYSTEM_PROMPT}\n{question}?"""
        with st.spinner("Please wait. Generating response..."):
            response = self.pipeline(prompt)
            self.stream_container.markdown(response)
        self.log(question, response, prompt)
        return response
