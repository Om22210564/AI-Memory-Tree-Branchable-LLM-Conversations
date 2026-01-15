import os
from groq import Groq

_client = None
API_KEY = ""  # ⚠️ not recommended for production

def get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=API_KEY)
    return _client

def generate_response(prompt: str) -> str:
    """Call Groq chat completion with the provided prompt.

    Returns the model response text or raises an exception on error.
    """
    client = get_client()
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
        )
        # The shape of completion may vary; handle common patterns
        # Prefer returned content in completion.choices[0].message.content
        if hasattr(completion, 'choices') and len(completion.choices) > 0:
            choice = completion.choices[0]
            # some clients return message dict
            message = getattr(choice, 'message', None)
            if message is None and isinstance(choice, dict):
                message = choice.get('message')
            if message:
                return message.get('content') if isinstance(message, dict) else message.content

        # Fallback: try to stringify
        return str(completion)
    except Exception as e:
        # Return an error-like response so the node records the failure
        return f"[LLM error] {str(e)}"

def summarize_node(prompt: str, response: str) -> str:
    """Summarize a node's prompt and response into max 250 characters.
    
    Uses system prompt to instruct LLM to keep summary concise.
    """
    client = get_client()
    try:
        text_to_summarize = f"Q: {prompt}\nA: {response}"
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a summarization expert. Summarize the following Q&A in exactly 250 characters or less. Be concise and capture the main idea."
                },
                {"role": "user", "content": text_to_summarize}
            ],
        )
        if hasattr(completion, 'choices') and len(completion.choices) > 0:
            choice = completion.choices[0]
            message = getattr(choice, 'message', None)
            if message is None and isinstance(choice, dict):
                message = choice.get('message')
            if message:
                content = message.get('content') if isinstance(message, dict) else message.content
                # Ensure we don't exceed 250 chars
                return content[:250]
        return text_to_summarize[:250]
    except Exception as e:
        # Fallback: truncate original text
        fallback = f"Q: {prompt}\nA: {response}"
        return fallback[:250]
