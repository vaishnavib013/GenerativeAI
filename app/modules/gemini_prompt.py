# app/modules/gemini_prompt.py

import requests
import json
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyD0Pb34j1erRQlw9yGpWtlZZczh2r1sYO0"

def generate_swot(scraped_data):
    try:
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent"
        headers = {"Content-Type": "application/json"}

        scraped_data = scraped_data[:3000]  # Limit input size
        prompt = (
            "You are an AI analyst. Based on the following company description, provide a concise SWOT analysis.\n\n"
            f"{scraped_data}\n\n"
            "Format your response as:\n\n"
            "Strengths:\n- ...\n\nWeaknesses:\n- ...\n\nOpportunities:\n- ...\n\nThreats:\n- ..."
        )

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ]
        }

        response = requests.post(f"{url}?key={GEMINI_API_KEY}", headers=headers, data=json.dumps(payload))
        data = response.json()

        print(json.dumps(data, indent=2))  # Optional for debugging

        candidates = data.get("candidates", [])
        if not candidates:
            return "⚠️ Error: No candidates returned from Gemini API."

        content = candidates[0].get("content", {})
        parts = content.get("parts", [])
        if not parts:
            return "⚠️ Error: No content parts found in Gemini API response."

        return parts[0].get("text", "⚠️ Error: No text returned in response part.")
    
    except Exception as e:
        return f"⚠️ Exception: {str(e)}"