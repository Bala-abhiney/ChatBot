import requests
import re

# ✅ Use your actual Gemini API key
GEMINI_API_KEY = "AIzaSyANG5DjGcMWztbQqkV2b8UD9bnDEm3M_M0"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

def validate_answers(answers):
    headers = {
        "Content-Type": "application/json"
    }

    # Construct prompt with all answers
    prompt = (
        "You are an AI evaluator. You will be given a set of technical questions and a candidate's answers. "
        "Your task is to evaluate all answers together and assign an overall score out of 100 based on their correctness, depth, clarity, and relevance. "
        "Also consider penalizing usage of built-in methods where implementation was expected. "
        "Please return the total score in the format: 'Score: <number>' followed by brief overall feedback.\n\n"
        "Here are the answers:\n"
    )

    for key, answer in answers.items():
        answer = answer.strip()
        if not answer:
            return {"score": 0, "feedback": "Please answer all the questions before submitting."}
        prompt += f"{key}: {answer}\n"

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        parts = result.get("candidates", [])[0].get("content", {}).get("parts", [])
        response_text = parts[0].get("text", "") if parts else "No feedback provided."

        # Extract score
        score_match = re.search(r"Score[:\s]+(\d+)", response_text, re.IGNORECASE)
        score = int(score_match.group(1)) if score_match else 0
        feedback = response_text.replace(score_match.group(0), "").strip() if score_match else response_text

        return {
            "score": score,
            "feedback": feedback
        }

    except Exception as e:
        print(f"Error during validation: {e}")
        return {
            "score": 0,
            "feedback": "Error validating answers. Please try again."
        }

# print(validate_answers({"answer_1": "python : list is a good datatype"}))