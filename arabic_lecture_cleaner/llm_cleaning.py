import ollama
import requests
from loguru import logger
from openai import OpenAI



def generate_messages(instruction_prompt: str, text_to_process: str):
    return [
        {"role": "system", "content": instruction_prompt},
        {
            "role": "user",
            "content": "En suivant les instructions données, traite ce cours: [DEBUT DU COURS]"
            + text_to_process
            + "[FIN DU COURS]",
        },
    ]


def process_text_ollama_api(instruction_prompt: str, text_to_process: str, model: str):
    """
    Process text using specific instructions via Ollama.

    Args:
        instruction_prompt: Instructions defining the model's role/behavior
        text_to_process: The actual text to operate on
        model: Ollama model name
    """
    messages = generate_messages(instruction_prompt, text_to_process)

    logger.debug(messages)
    response = ollama.chat(model=model, messages=messages)
    return response["message"]["content"]


def process_text_openai_api(
    instruction_prompt: str,
    text_to_process: str,
    model: str,
    api_base: str,
    api_key: str,
):
    """
    Process text using specific instructions via Mammouth AI API.

    Args:
        instruction_prompt: Instructions defining the model's role/behavior
        text_to_process: The actual text to operate on
        model: Model name
    """
    client = OpenAI(base_url=api_base, api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=generate_messages(instruction_prompt, text_to_process),
    )
    logger.debug(response)
    text_response = " - ".join(
        [choice["message"]["content"] for choice in response["choices"]]
    )
    logger.info(f"Total used tokens: {response['usage']['total_tokens']}")

    return text_response


def process_text_mammouth_api(
    instruction_prompt: str,
    text_to_process: str,
    model: str,
    api_base: str,
    api_key: str,
):
    """
    Process text using specific instructions via Mammouth AI API.

    Args:
        instruction_prompt: Instructions defining the model's role/behavior
        text_to_process: The actual text to operate on
        model: Model name
    """
    if api_key is None:
        raise ValueError("Please set a mammouth api key in your environment.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model,
        "messages": generate_messages(instruction_prompt, text_to_process),
    }
    response = requests.post(api_base, headers=headers, json=data).json()
    logger.debug(response)
    text_response = " - ".join(
        [choice["message"]["content"] for choice in response["choices"]]
    )
    logger.info(f"Total used tokens: {response['usage']['total_tokens']}")

    return text_response
