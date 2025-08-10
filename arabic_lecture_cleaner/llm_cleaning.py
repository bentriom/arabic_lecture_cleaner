import ollama
import requests
from loguru import logger

import arabic_lecture_cleaner.constants as const


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


def process_text_local(instruction_prompt: str, text_to_process: str, model: str):
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


def process_text_mammouth_api(
    instruction_prompt: str, text_to_process: str, model: str
):
    """
    Process text using specific instructions via Mammouth AI API.

    Args:
        instruction_prompt: Instructions defining the model's role/behavior
        text_to_process: The actual text to operate on
        model: Model name
    """
    if const.MAMMOUTH_API_KEY is None:
        raise ValueError("Please set a mammouth api key in your environment.")

    headers = {
        "Authorization": f"Bearer {const.MAMMOUTH_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model,
        "messages": generate_messages(instruction_prompt, text_to_process),
    }
    response = requests.post(const.MAMMOUTH_API_URL, headers=headers, json=data).json()
    logger.debug(response)
    text_response = " - ".join(
        [choice["message"]["content"] for choice in response["choices"]]
    )
    logger.info(f"Total used tokens: {response['usage']['total_tokens']}")

    return text_response
