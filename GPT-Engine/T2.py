import openai
import os

# Set your API key
openai.api_key = os.environ["OPENAI_PERSONAL_KEY"]

def generate_response(prompt, model="gpt-3.5-turbo", max_tokens=4000, batch_size=5):
    """
    Generate a response from OpenAI's GPT model based on the input prompt.

    Parameters:
    - prompt (str): The text prompt to generate a response for.
    - model (str): The GPT model to use (default is 'gpt-4').
    - max_tokens (int): Maximum number of tokens in the generated response.

    Returns:
    - str: The generated response from the model.
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        # Extract the message content from the response
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Example Usage
if __name__ == "__main__":
    user_prompt = "You are an AI agent expert. Generate 50 types of complex AI agents that can be built."
    response = generate_response(user_prompt)
    print("Generated Response:")
    print(response)
