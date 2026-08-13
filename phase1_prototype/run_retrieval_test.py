import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b-instruct"

# A simulated retrieval payload containing a mix of correct and incorrect codes
CANDIDATE_CODES = [
    {"code": "E11.9", "description": "Type 2 diabetes mellitus without complications"},
    {"code": "J45.901", "description": "Unspecified asthma with (acute) exacerbation"},
    {"code": "I10", "description": "Essential (primary) hypertension"},
    {"code": "K35.80", "description": "Unspecified acute appendicitis"},
    {"code": "S52.521A", "description": "Torus fracture of lower end of right radius, initial encounter, closed fracture"}
]

def run_retrieval_test():
    with open('sample_notes.json', 'r') as f:
        notes = json.load(f)

    for note in notes:
        prompt = f"""
        You are a clinical extraction assistant. 
        Read the Clinical Note. Then, evaluate the provided JSON list of Candidate Codes.
        For each candidate code, determine if there is a related mention in the clinical note.
        
        Return a JSON array of objects containing 'code' and a boolean 'is_mentioned' (true or false).
        
        Candidate Codes: {json.dumps(CANDIDATE_CODES)}
        
        Clinical Note: {note['text']}
        """
        
        payload = {
            "model": MODEL,
            "prompt": prompt,
            "format": "json",
            "stream": False
        }
        
        response = requests.post(OLLAMA_URL, json=payload).json()
        print(f"--- Retrieval-Framing Output for {note['id']} ---")
        try:
            print(json.dumps(json.loads(response['response']), indent=2))
        except:
            print("Failed to parse JSON.")

if __name__ == "__main__":
    run_retrieval_test()