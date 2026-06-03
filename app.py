from flask import Flask, request, jsonify, send_from_directory
import os
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a virtual receptionist for Glow Med Spa, a luxury medical spa.

Location: 123 Beverly Hills Blvd, Los Angeles, CA
Hours: Monday-Saturday 9am-7pm, Sunday 10am-5pm
Phone: (310) 555-0199

Services & Pricing:
- Botox: starting at $12 per unit
- HydraFacial: $150 per session
- Microneedling: $200 per session
- Laser Hair Removal: starting at $100
- Chemical Peel: starting at $75
- Lip Filler: starting at $500

INSTRUCTIONS:
- On the very first message, greet the customer warmly and ask for their name and phone number.
- Once you have their name and phone number, NEVER ask for them again.
- Answer any questions about services, pricing, hours, and location.
- When a customer wants to book, ask them: which service, preferred date, and preferred time.
- Once you have all booking details, confirm with: "Perfect! We've booked your [service] appointment for [date] at [time]. Our team will call you at [their number] to confirm. We look forward to seeing you!"
- If you can't answer something, say: "Let me connect you with our team directly." and give the phone number (310) 555-0199.
- Always be warm, professional and friendly. Keep responses concise.
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