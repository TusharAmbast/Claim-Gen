import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:14b-instruct"

CANDIDATE_CODES = [
    {"code": "E11.9", "description": "Type 2 diabetes mellitus without complications"},
    {"code": "J45.901", "description": "Unspecified asthma with (acute) exacerbation"},
    {"code": "I10", "description": "Essential (primary) hypertension"},
    {"code": "K35.80", "description": "Unspecified acute appendicitis"},
    {"code": "S52.521A", "description": "Torus fracture of lower end of right radius, initial encounter, closed fracture"}
]

def run_retrieval_test_v2():
    with open('sample_notes.json', 'r') as f:
        notes = json.load(f)

    for note in notes:
        prompt = f"""
        You are a clinical extraction assistant.
        Analyze the Clinical Note against the provided candidate ICD-10 codes.
        
        For EACH candidate code, perform the following two steps:
        1. Extract relevant quote/evidence from the text (or write "None").
        2. Set 'is_mentioned' to true if the clinical note directly supports, diagnoses, suspects, or references this condition in patient history. Otherwise false.

        Return ONLY a JSON object with a 'evaluations' array containing objects with keys:
        'code', 'evidence_quote', 'reasoning', 'is_mentioned'.

        Candidate Codes: {json.dumps(CANDIDATE_CODES)}

        Clinical Note: {note['text']}
        """
        
        payload = {
            "model": MODEL,
            "prompt": prompt,
            "format": "json",
            "stream": False
        }
        
        api_response = requests.post(OLLAMA_URL, json=payload).json()
        print(f"--- CoT Retrieval Output for {note['id']} ---")
        
        # Check if Ollama returned an error directly
        if 'error' in api_response:
            print(f"❌ Ollama Server Error: {api_response['error']}")
            continue

        try:
            raw_output = api_response.get('response', '')
            
            # Sanitize: Remove markdown formatting if the model included it
            if raw_output.startswith("```json"):
                raw_output = raw_output.replace("```json", "", 1)
                raw_output = raw_output.rsplit("```", 1)[0]
            elif raw_output.startswith("```"):
                raw_output = raw_output.replace("```", "", 1)
                raw_output = raw_output.rsplit("```", 1)[0]
                
            raw_output = raw_output.strip()
            
            # Now try to parse
            parsed_json = json.loads(raw_output)
            print(json.dumps(parsed_json, indent=2))
            
        except Exception as e:
            print(f"❌ Failed to parse JSON: {e}")
            print(f"--- Raw Output (so we can see what broke it) ---")
            print(raw_output)

if __name__ == "__main__":
    run_retrieval_test_v2()