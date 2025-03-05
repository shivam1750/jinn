import os
import time
import random
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
)

initial_prompt = """
You are a historical agent AI. You can answer questions about historical monuments around the world.
If you'd like, you can also send detailed information by email — just share your email address and I'll verify it with an OTP.
"""


chat_session = model.start_chat(history=[])
response = chat_session.send_message(initial_prompt)
print(response.text)

def send_otp(email):
    otp = str(random.randint(100000, 999999))
    print(f"[Simulated] OTP sent to {email}: {otp}")
    return otp

otp_sent = False
expected_otp = ""
email = ""
while True:
    user_input = input("User: ")
    if "email" in user_input.lower():
        print("Bot: Please share your email address.")
    elif "@" in user_input:
        email = user_input
        expected_otp = send_otp(email)
        otp_sent = True
        print("Bot: I've sent a 6-digit code to your email. Please confirm the code.")
    elif otp_sent and user_input.isdigit():
        if user_input == expected_otp:
            print("Bot: Great! Your email has been verified. I’ll shoot you an email soon. Take care!")
            break
        else:
            print("Bot: Sorry, that's incorrect. Can you please check again?")
    elif "bye" in user_input.lower() or "exit" in user_input.lower():
        print("Bot: Take care! If you’d like more recommendations, just reach out again.")
        break
    else:
        response = chat_session.send_message(user_input)
        print(f"Bot: {response.text}")
