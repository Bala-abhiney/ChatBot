# question_generator.py

import requests

# ✅ Use your actual Gemini API key
GEMINI_API_KEY = "AIzaSyCZC2GgmmFhQwl6PLCJ-UxwCHVxz3ybz4E"

# ✅ Key is passed via URL query 
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

def generate_questions(tech_stack):
    questions = {}  

    for tech in tech_stack:
        prompt = f"Generate 3 random basic interview questions for a candidate proficient in {tech}"
        f"if it is coding question provide sample output with input example within the question dont take it in saparate line."
        f"dont give explanation for questions and also user should not use builtin methods"
        f"give random questions with shuffle"

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(GEMINI_URL, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

            # Extract and clean up the response
            parts = result.get("candidates", [])[0].get("content", {}).get("parts", [])
            # print(parts)
            response_text = parts[0].get("text", "") if parts else "(No response)"
            # print(response_text)
            question_lines = [line.strip("-• ") for line in response_text.strip().split("\n") if line.strip()]
            questions[tech] = question_lines  # Store under tech name

        except Exception as e:
            print(f"Error generating questions for {tech}: {e}")
            questions[tech] = [f"(Error generating questions for {tech})"]

    return questions



# print(generate_questions(["python"]))
