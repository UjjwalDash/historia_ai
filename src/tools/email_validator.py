import smtplib
import random
import os
import json
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables
load_dotenv("src/config/tools/.email_env")

def generate_otp(length=6):
    """Generates a random OTP of given length."""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def save_otp_json(receiver_email, otp):
    """Saves OTP and receiver email to a JSON file."""
    data = {"receiver_email": receiver_email, "otp": otp}
    with open("temp.json", "w") as file:
        json.dump(data, file)

def email_validator(receiver_email):
    """
    Sends an OTP to the given email and saves it to otp_data.json.

    Args:
        receiver_email (str): Email of the receiver.
    Returns:
        str: A formatted string containing confirmation message.
    """

    sender_email = os.getenv("EMAIL_SENDER")  # Your email
    sender_password = os.getenv("EMAIL_PASSWORD")  # App password

    otp = generate_otp()
    save_otp_json(receiver_email, otp)  # Save OTP to JSON file

    subject = "Your OTP Code"
    body = f"Your One-Time Password (OTP) is: {otp}\n\nUse this to complete your authentication. It is valid for a limited time."

    msg = MIMEText(body)
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"OTP sent successfully to {receiver_email}")
        return f"OTP sent successfully to {receiver_email}"
    except Exception as e:
        print(f"Error sending OTP: {e}")
        return f"Error sending OTP: {e}"

# # Example Usage
# otp = email_validator("dashujjwaldash@gmail.com")
# print("Generated OTP:", otp)
