from flask import Flask, request, jsonify, send_from_directory
from groq import Groq

app = Flask(__name__)

import os
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a helpful assistant for Glow Med Spa, a luxury medical spa.

Location: 123 Beverly Hills Blvd, Los Angeles, CA
Hours: Monday-Saturday 9am-7pm, Sunday 10am-5pm
Phone: (310) 555-0199
Booking: https://calendly.com/glowmedspa

Services & Pricing:
- Botox: starting at $12 per unit
- HydraFacial: $150 per session
- Microneedling: $200 per session
- Laser Hair Removal: starting at $100
- Chemical Peel: starting at $75
- Lip Filler: starting at $500

IMPORTANT INSTRUCTIONS:
- When a customer first messages you, before answering anything, warmly greet them and ask for their name and phone number so the team can follow up with them personally.
- Once they provide their name and phone number, thank them and then help them with their question.
- If they want to book, share the booking link: https://calendly.com/glowmedspa
- If they ask something you don't know, say: "That's a great question! Let me connect you with one of our specialists." and provide the phone number (310) 555-0199.
- Always be warm, professional and friendly.
- Keep responses concise.
"""

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
   history = request.json.get("history", [])
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        *history,
        {"role": "user", "content": user_message}
    ]
)
    return jsonify({"reply": response.choices[0].message.content})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860, debug=False)