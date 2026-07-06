import ollama


def get_answer(prompt):
    """
    Sends the prompt to the LLM and returns the generated answer.
    """

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response["message"]["content"]

    return answer