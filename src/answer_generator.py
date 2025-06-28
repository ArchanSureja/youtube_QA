

def generate_answer(model, context, question):
    """
    Uses the passed genai.Client to generate an answer using Gemini model.

    Parameters:
    - client: an instance of genai.Client (not the model itself)
    - context: combined text chunks as a single string
    - question: user input

    Returns:
    - A string containing the generated answer
    """
    try:
        prompt = f"""Answer the following question based on the given context.

Context:
{context}

Question:
{question}

Answer:"""

        response = model.generate_content(prompt)

        if response and hasattr(response, "text"):
            return response.text.strip()

    except Exception as e:
        print(f"[generate_answer error] {e}")

    return None
