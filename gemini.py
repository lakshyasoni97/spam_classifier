import google.generativeai as genai
import json
import re

def get_gemini_response(input, prompt, gemini_api_key, temperature = 0.9):
    # gemini_api_key = ''
    genai.configure(api_key=gemini_api_key)
    generation_config = {
        "temperature": temperature,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                    generation_config=generation_config)

    response = model.generate_content([input, prompt])
    return response.text