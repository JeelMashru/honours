import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from local environment configuration
load_dotenv()

# Initialize OpenAI-compatible Client (Configured for Groq Cloud Endpoint)
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def generate_text_with_parameters(prompt: str, temp: float, top_p: float, freq_penalty: float):
    """
    Executes an API call with dynamic sampling hyperparameters.
    """
    print("=" * 65)
    print(f"Testing Parameters: Temp={temp} | Top_P={top_p} | Frequency_Penalty={freq_penalty}")
    print("=" * 65)

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful engineering assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temp,
            top_p=top_p,
            frequency_penalty=freq_penalty,
            max_tokens=150
        )
        
        output_text = response.choices[0].message.content
        print(f"Output:\n{output_text}\n")
        return output_text

    except Exception as e:
        print(f"An error occurred during API execution: {e}")

if __name__ == "__main__":
    test_prompt = "Write a three-sentence intro for a novel about an autonomous robot studying ocean ecosystems."

    # Run 1: Deterministic Mode
    generate_text_with_parameters(test_prompt, temp=0.0, top_p=0.1, freq_penalty=0.0)

    # Run 2: High Variance / Creative Mode
    generate_text_with_parameters(test_prompt, temp=1.2, top_p=0.95, freq_penalty=0.0)

    # Run 3: Applied Frequency Penalty Mode
    generate_text_with_parameters(test_prompt, temp=0.7, top_p=0.8, freq_penalty=1.5)