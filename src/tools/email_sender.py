import smtplib
import os
import time
from email.mime.text import MIMEText
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from src.models.models import query_llm
from dotenv import load_dotenv
import json
# Load environment variables
load_dotenv("src/config/tools/.email_env")

def email_sender(otp: str, question: str) -> str:
    """
    Sends trip information to the given email ONLY after validating OTP.
    REQUIRES: The user must have entered an OTP in their last message.

    Args:
        otp (str): OTP provided by the user - MUST match the stored OTP
        question (str): question asked by the user

    Returns:
        str: A formatted string containing confirmation message or error.
    """
    system = """
    You are a helpful assistant. You are an expert in answering questions related to historical monuments across the world.
    And provide proper plan for visiting the places.
    """
    human = f"Provide a proper plan for the user query {question}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    chain = prompt | query_llm
    result = chain.invoke({"text": "Explain the importance of low latency LLMs."})
    
    # STRICT OTP VERIFICATION
    try:
        with open("temp.json", "r") as file:
            data = json.load(file)
        # with open("temp.txt", "r") as file:
            stored_otp = data['otp']
            receiver_email = data['receiver_email']
            stored_time = os.path.getmtime("temp.json")
            
        # Check if OTP file is recent (within last 10 minutes)
        if time.time() - stored_time > 600:  # 10 minutes
            return "ERROR: OTP has expired. Please request a new OTP."
            
        # Verify OTP strictly
        if not stored_otp or stored_otp != otp:
            return "ERROR: OTP verification failed. Please enter the correct OTP that was sent to your email."
    except FileNotFoundError:
        return "ERROR: No OTP has been generated. Please request an OTP first."

    # Format the plan as plain text - avoid nested quotes and escape characters
    clean_plan = result.content.replace("\\'", "'").replace('\\"', '"').replace('\\n', '\n')
    
    # Only proceed if OTP verification passes
    sender_email = os.getenv("EMAIL_SENDER")
    sender_password = os.getenv("EMAIL_PASSWORD")
    
    subject = "Historical Places to Visit"
    body = f"Here is your personalized trip plan with historical places to visit:\n\n{clean_plan}"

    msg = MIMEText(body)
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        
        # Delete the temp.txt file after successful verification
        # os.remove("temp.txt")
            
        return f"SUCCESS: Your trip information has been sent successfully to {receiver_email}"
    except Exception as e:
        return f"ERROR: Failed to send email: {str(e)}"

# print(email_sender("832070", "currently i am in mumbai"))