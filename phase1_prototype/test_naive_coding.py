import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b-instruct"

def run_naive_test():
    with open('sample_notes.json', 'r') as f:
        notes = json.load(f)

    for note in notes:
        prompt = f"""
        You are a clinical coder. Read the following clinical note and assign the correct ICD-10-CM codes.
        Return ONLY a JSON array of objects with 'code' and 'description' keys.
        
        Clinical Note: {note['text']}
        """
        
        payload = {
            "model": MODEL,
            "prompt": prompt,
            "format": "json",
            "stream": False
        }
        
        response = requests.post(OLLAMA_URL, json=payload).json()
        print(f"--- Naive Output for {note['id']} ---")
        try:
            print(json.dumps(json.loads(response['response']), indent=2))
        except:
            print("Failed to parse JSON.")

if __name__ == "__main__":
    run_naive_test()