import ollama

from loguru import logger


def process_text_local(instruction_prompt: str, text_to_process: str, model: str):
    """
    Process text using specific instructions via Ollama.
    
    Args:
        instruction_prompt: Instructions defining the model's role/behavior
        text_to_process: The actual text to operate on
        model: Ollama model name
    """
    messages = [
        {
            'role': 'system', 
            'content': instruction_prompt
        },
        {
            'role': 'user', 
            'content': 'Traite ce texte: ' + text_to_process
        }
    ]
    
    logger.debug(messages)
    response = ollama.chat(model=model, messages=messages)
    return response['message']['content']
