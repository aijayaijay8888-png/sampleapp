# filename: mistral_chat_bot.py
# Save this as app.py if you want to run it easily: python app.py

!pip install mistralai

from mistralai import Mistral

# ⚠️ Directly embedding API keys is unsafe for sharing/production.
# For local testing only.
API_KEY = "5y9uaQXlvqH9dR3tVxxSsdl07G1ujJjw"

client = Mistral(api_key=API_KEY)
MODEL = "mistral-large-latest"

system_prompt = "You are a friendly assistant. Keep answers short and helpful."

def chat_once(user_message: str) -> str:
    resp = client.chat.complete(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=400
    )
    return resp.choices[0].message.content

if __name__ == "__main__":
    print("Mistral Bot 🤖  (type 'exit' to quit)")
    while True:
        msg = input("You: ").strip()
        if msg.lower() in {"exit", "quit"}:
            break
        answer = chat_once(msg)
        print("Bot:", answer)
