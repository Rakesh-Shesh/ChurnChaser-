import openai
import os

openai.api_key = os.environ.get("OPENAI_PERSONAL_KEY", "your-openai-api-key")  # Replace if needed

# Function to read AI agents from file
def read_ai_agents(filename=r'C:\Users\User\Desktop\AI agents\GPT-Engine\Agents\AIagents.txt'):
    try:
        with open(filename, 'r') as file:
            agents = file.readlines()
        return [agent.strip() for agent in agents]
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []

# Function to generate code for each agent using GPT-4
def generate_agent_code(agent_name):
    prompt = f"Generate Python code for an AI agent named '{agent_name}'. This should be a well-structured and complete Python script."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Ensure GPT-4 access
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7,
            n=1
        )
        code = response['choices'][0]['message']['content'].strip()
        return code
    except openai.error.RateLimitError as e:
        print(f"Rate limit error for {agent_name}: {e}")
    except openai.error.APIConnectionError as e:
        print(f"API connection error for {agent_name}: {e}")
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error for {agent_name}: {e}")
    except Exception as e:
        print(f"Error generating code for {agent_name}: {e}")
    return None

# Function to save code in the appropriate folder
def save_agent_code(agent_name, code, base_dir="AI-Agents-Repo/agent_codes"):
    agent_folder = os.path.join(base_dir, agent_name.lower().replace(" ", "_"))
    os.makedirs(agent_folder, exist_ok=True)  # Avoid errors if folder already exists

    code_filename = os.path.join(agent_folder, f"{agent_name.replace(' ', '_')}_agent.py")
    with open(code_filename, 'w') as code_file:
        code_file.write(code)
    print(f"Code for {agent_name} saved in {code_filename}")

# Main function to process all agents
def generate_and_save_agents():
    agents = read_ai_agents()
    for agent in agents:
        print(f"Generating code for {agent}...")
        code = generate_agent_code(agent)
        if code:
            save_agent_code(agent, code)

# Run the function
if __name__ == "__main__":
    generate_and_save_agents()
