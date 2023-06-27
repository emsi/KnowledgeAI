import warnings
from typing import Any, Dict, Tuple

import streamlit as st
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

import chat
from config import settings

INSTRUCTION_KEY = "### Instruction:"
RESPONSE_KEY = "### Response:"
END_KEY = "### End"
INTRO_BLURB = "Below is an instruction that describes a task. Write a response that appropriately completes the request."
PROMPT_FOR_GENERATION_FORMAT = """{intro}
{instruction_key}
{instruction}
{response_key}
""".format(
    intro=INTRO_BLURB,
    instruction_key=INSTRUCTION_KEY,
    instruction="{instruction}",
    response_key=RESPONSE_KEY,
)


# Define a function to load the large language model
@st.cache_resource(show_spinner="Please wait. Loading ML model...")
def load_large_language_model(
    model_name, torch_dtype=None, trust_remote_code=None, use_auth_token=None, padding_side="left"
):
    """Load the large language model and tokenizer."""
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch_dtype,
        trust_remote_code=trust_remote_code,
        use_auth_token=use_auth_token,
        low_cpu_mem_usage=True,
    )
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        trust_remote_code=trust_remote_code,
        use_auth_token=use_auth_token,
        padding_side=padding_side,
    )
    return model, tokenizer


class InstructionTextGenerationPipeline:
    def __init__(
        self,
        model_name,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
        use_auth_token=None,
    ) -> None:
        self.model, self.tokenizer = load_large_language_model(
            model_name,
            torch_dtype=torch_dtype,
            trust_remote_code=trust_remote_code,
            use_auth_token=use_auth_token,
            padding_side="left",
        )
        if self.tokenizer.pad_token_id is None:
            warnings.warn(
                "pad_token_id is not set for the tokenizer. Using eos_token_id as pad_token_id."
            )
            self.tokenizer.pad_token = self.tokenizer.eos_token

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # self.model.eval()
        self.model.to(device=device, dtype=torch_dtype)

        self.generate_kwargs = {
            "temperature": 0.1,
            "top_p": 0.92,
            "top_k": 0,
            "max_new_tokens": 1024,
            "use_cache": True,
            "do_sample": True,
            "eos_token_id": self.tokenizer.eos_token_id,
            "pad_token_id": self.tokenizer.pad_token_id,
            "repetition_penalty": 1.1,  # 1.0 means no penalty, > 1.0 means penalty, 1.2 from CTRL paper
        }

    def format_instruction(self, instruction):
        return PROMPT_FOR_GENERATION_FORMAT.format(instruction=instruction)

    def __call__(
        self, instruction: str, **generate_kwargs: Dict[str, Any]
    ) -> Tuple[str, str, float]:
        s = PROMPT_FOR_GENERATION_FORMAT.format(instruction=instruction)
        input_ids = self.tokenizer(s, return_tensors="pt").input_ids
        input_ids = input_ids.to(self.model.device)
        gkw = {**self.generate_kwargs, **generate_kwargs}
        with torch.no_grad():
            output_ids = self.model.generate(input_ids, **gkw)
        # Slice the output_ids tensor to get only new tokens
        new_tokens = output_ids[0, len(input_ids[0]) :]
        output_text = self.tokenizer.decode(new_tokens, skip_special_tokens=True)
        return output_text


class Chat(chat.Chat):
    """Chatbot class implemented using MosaicML MPT"""

    def __init__(self, stream_container):
        self.response = ""
        self.stream_container = stream_container
        # Initialize the model and tokenizer
        self.pipeline = InstructionTextGenerationPipeline(
            settings.MODEL,
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
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
