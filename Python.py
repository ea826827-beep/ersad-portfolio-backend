from flask import Flask, request, jsonify
from flask_cors import CORS
from email.message import EmailMessage
import smtplib
import os
import re

app = Flask(__name__)

# Allow your GitHub Pages frontend to call this API
CORS(app)

MY_EMAIL = "ersad1650@gmail.com"


def is_valid_email(email):
    pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    return re.match(pattern, email) is not None


@app.get("/")
def home():
    return jsonify({
        "status": "online",
        "message": "Ersad Portfolio Backend is running"
    })


@app.post("/contact")
def contact():

    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "success": False,
                "message": "Invalid request."
            }), 400

        name = str(data.get("name", "")).strip()
        visitor_email = str(data.get("email", "")).strip()
        subject = str(data.get("subject", "")).strip()
        message = str(data.get("message", "")).strip()

        if not name:
            return jsonify({
                "success": False,
                "message": "Name is required."
            }), 400

        if not is_valid_email(visitor_email):
            return jsonify({
                "success": False,
                "message": "Please enter a valid email."
            }), 400

        if not message:
            return jsonify({
                "success": False,
                "message": "Message is required."
            }), 400

        app_password = os.getenv("uhla mqfw soti sfob")

        if not app_password:
            return jsonify({
                "success": False,
                "message": "Email service is not configured."
            }), 500

        mail = EmailMessage()

        mail["From"] = MY_EMAIL
        mail["To"] = MY_EMAIL
        mail["Reply-To"] = visitor_email
        mail["Subject"] = subject or "Portfolio Contact Message"

        mail.set_content(
            f"""New Portfolio Message

Name: {name}
Visitor Email: {visitor_email}
Subject: {subject}

Message:
{message}
"""
        )

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as smtp:

            smtp.login(
                MY_EMAIL,
                app_password
            )

            smtp.send_message(mail)

        return jsonify({
            "success": True,
            "message": "Message sent successfully!"
        })

    except smtplib.SMTPAuthenticationError:

        return jsonify({
            "success": False,
            "message": "Email authentication failed."
        }), 500

    except Exception as error:

        print("SERVER ERROR:", error)

        return jsonify({
            "success": False,
            "message": "Server error."
        }), 500


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )