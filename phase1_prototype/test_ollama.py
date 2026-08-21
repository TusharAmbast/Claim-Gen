import requests
import json
import sys

# Ollama default API endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b-instruct"

# ~10 varied prompts testing different extraction and formatting tasks
prompts = [
    "Extract the patient name and age from this sentence: 'John Doe is a 45 year old male.' Return as JSON with keys 'name' and 'age'.",
    "List three common symptoms of flu in JSON format with a 'symptoms' array.",
    "Return a simple JSON object with 'status': 'success' and 'code': 200.",
    "Patient complains of severe lower back pain radiating down the left leg. Extract the symptom and location into a JSON object.",
    "Generate a JSON object containing a fake patient's demographic data (name, DOB, gender).",
    "Analyze this text: 'Prescribed 500mg Amoxicillin twice daily.' Return a JSON with keys 'medication', 'dosage', and 'frequency'.",
    "Create a nested JSON where the top key is 'diagnoses' containing an array of two objects, each with 'condition' and 'severity' keys.",
    "Parse this: 'Blood pressure is 120/80, heart rate is 75.' Output JSON with 'vitals' as the root key.",
    "Output an empty JSON object.",
    "Respond ONLY with a JSON array containing the numbers 1 through 5."
]

def run_tests():
    print(f"Starting Phase 0 Sanity Check against {MODEL}...\n")
    success_count = 0

    for i, prompt in enumerate(prompts, 1):
        payload = {
            "model": MODEL,
            "prompt": prompt,
            "format": "json", # This is the critical parameter Ollama uses to constrain output
            "stream": False
        }
        
        try:
            response = requests.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            result = response.json()
            
            raw_output = result.get('response', '')
            
            # The real test: Will Python's json parser choke on the output?
            parsed_content = json.loads(raw_output)
            print(f"✅ Test {i} PASSED")
            print(f"   Output: {json.dumps(parsed_content)}\n")
            success_count += 1
            
        except json.JSONDecodeError:
            print(f"❌ Test {i} FAILED: Model did not return valid JSON.")
            print(f"   Raw Output: {raw_output}\n")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Test {i} ERROR: Could not reach Ollama API. Is it running? Details: {e}\n")
            sys.exit(1)

    print("-" * 40)
    print(f"Results: {success_count}/{len(prompts)} prompts successfully returned parseable JSON.")
    
    if success_count == len(prompts):
        print("EXIT CRITERIA MET: You are cleared to proceed to Phase 1.")
    else:
        print("EXIT CRITERIA FAILED: Do not pass go. Troubleshoot prompting or update the model.")

if __name__ == "__main__":
    run_tests()