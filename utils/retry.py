import time

import ollama


def retry_with_backoff(operation, max_retries=2, base_delay=1):
    for attempt in range(max_retries + 1):
        try:
            return operation()
        except Exception:
            if attempt == max_retries:
                raise

            delay = base_delay * (2 ** attempt)
            time.sleep(delay)


result = retry_with_backoff(
    lambda: ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": "What is diabetes?"
            }
        ]
    )
)