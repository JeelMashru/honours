import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load environment variables
load_dotenv()

# 2. Initialize Client (Points to Groq Cloud API or OpenAI)
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"  # ✅ Clean URL string
)
def extract_structured_json(unstructured_text: str):
    """
    Uses a constrained system prompt to extract unstructured text into strict JSON.
    """
    
    system_prompt = """
    You are an automated Data Extraction Engine.
    Your task is to extract information from unstructured engineering fault logs into a strict JSON object.

    OUTPUT RULES:
    - Return ONLY valid JSON.
    - No conversational preambles, post-explanations, or polite text.
    - If a field cannot be determined from the text, set its value to null.

    REQUIRED JSON SCHEMA:
    {
      "incident_id": "string or null",
      "equipment_name": "string",
      "failure_type": "string",
      "severity": "string (CRITICAL, MAJOR, MINOR)",
      "affected_subsystems": ["list of strings"],
      "recommended_action": "string"
    }
    """

    print("=" * 65)
    print("PROCESSING UNSTRUCTURED INPUT LOG...")
    print("=" * 65)
    print(f"Input Text:\n{unstructured_text.strip()}\n")

    try:
        # API Request with low temperature for deterministic parsing
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": unstructured_text}
            ],
            response_format={"type": "json_object"},  # Enforces pure JSON output at API level
            temperature=0.0,
            max_tokens=300
        )

        raw_output = response.choices[0].message.content.strip()

        # Strip markdown codeblock backticks if present
        cleaned_output = raw_output.replace("```json", "").replace("```", "").strip()

        print("-" * 65)
        print("RAW MODEL OUTPUT:")
        print(raw_output)
        print("-" * 65)

        # Programmatic Validation Test on cleaned string
        parsed_json = json.loads(cleaned_output)
        print("\n[SUCCESS] Programmatic Validation Passed! Valid JSON Object Created:")
        print(f"Equipment: {parsed_json.get('equipment_name')}")
        print(f"Severity:  {parsed_json.get('severity')}")
        print(f"Actions:   {parsed_json.get('recommended_action')}")

        return parsed_json

    except json.JSONDecodeError:
        print("\n[FAILED] Output failed JSON validation test!")
    except Exception as e:
        print(f"\nAn error occurred during API execution: {e}")

if __name__ == "__main__":
    
    # Messy, real-world unstructured log text
    sample_log = """
    URGENT LOG ENTRY - 02-AUG-2026 14:22 UTC
    System alert raised on High-Pressure Boiler Unit #4. Thermal sensors detected 
    overheating in the primary coolant intake loop and pressure relief valve B. 
    Operator logged issue under INC-88201. Severity classified as CRITICAL. 
    Immediate shutdown initiated and technician dispatch required to replace intake seals.
    """

    extract_structured_json(sample_log) 