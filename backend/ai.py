import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_keywords(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Extract genres, moods or artists from this prompt: '{prompt}'"}]
    )
    text = response['choices'][0]['message']['content']
    return [w.strip() for w in text.split(',') if w.strip()]
