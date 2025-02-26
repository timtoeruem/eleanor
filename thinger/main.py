from fastapi import FastAPI, HTTPException
import ollama
from email_agent import send_email
from calendar_agent import create_calendar_event
import re
from datetime import datetime, timedelta
from difflib import SequenceMatcher


def similar(a, b):
    ratio=SequenceMatcher(None, a, b).ratio()
    print(f"compared '{a}', '{b}'. ratio: {ratio}")
    return ratio

app = FastAPI()

# Function to call Ollama
def ai_chat(prompt):
    ollama_client = ollama.Client(host="localhost")
    response = ollama_client.chat(model="llama3.2-vision", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

# Extract event details using regex
def extract_event_details(response):
    event_pattern = r"schedule an event titled: (.+?) on: (.+?) at: (.+?) for: (.+?) hours with: (.+?)"
    #event_pattern = r"Schedule an event titled: [title] on: [YYYY-MM-DD] at: [HH:MM] for: [hours] hours with: [attendees]"
    match = re.search(event_pattern, response, re.IGNORECASE)

    if match:
        title = match.group(1).strip()
        date = match.group(2).strip()
        time = match.group(3).strip()
        duration = float(match.group(4).strip())
        attendees = match.group(5).strip().split(",") if match.group(5) else []

        # Convert to datetime format
        start_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        end_datetime = start_datetime + timedelta(hours=duration)

        return title, start_datetime.isoformat(), end_datetime.isoformat(), attendees

    return None, None, None, None

# Function to check if AI response indicates an email task
def extract_email_details(response):
    # Simple rule-based extraction (can be improved with better NLP)
    """
    'Send an email to timtoeruem@gmail.com with subject How to Boil Water and body:\n\n"Hello,\n\nBoiling water is a simple process that involves heating it to its boiling point. Here\'s a step-by-step guide on how to do it safely:\n\n1. Fill a pot with water from the tap.\n2. Place the pot on your stovetop over high heat.\n3. Wait for the water to reach its boiling point, indicated by large bubbles rising to the surface and steam escaping from the top.\n4. Once boiling, reduce the heat to a simmer (low-medium heat) to maintain the boil.\n\nThat\'s it! You can now use the boiled water for your intended purpose.\n\nBest regards,\n[Your Name]"'

    """
    email_pattern = r"send an email to (.+?) with subject (.+?) and body (.+)"
    email_pattern= r"To: (.+?) with subject: (.+?) and body: (.+)"
    match = re.search(email_pattern, response, re.IGNORECASE)
    
    if match:
        recipient = match.group(1).strip()
        subject = match.group(2).strip()
        body = match.group(3).strip()
        return recipient, subject, body
    return None, None, None

def extract_agent(response):
    agent_pattern = r"the agent that should be executing the task is: (.+)"
    match = re.search(agent_pattern, response, re.IGNORECASE)
    if match:
        agent = match.group(1).strip()
        return agent
    return None

#ideas
#turn on lights
#voice input&output

@app.post("/task")
async def handle_task(task: str):
    available_agents=['mail agent', 'calendar agent']
    ai_which_agent_response = ai_chat(f"the available agent names are: '{"','".join(available_agents)}'. Analyze this request and determine the agent that should be executing the task. format the answer as 'the agent that should be executing the task is: [agent name]', or just reply normally: {task}")
    agent_to_call = extract_agent(ai_which_agent_response)
    if agent_to_call == 'mail agent' or similar(agent_to_call, available_agents[0]) > 0.9:
        ai_response = ai_chat(f"Analyze the request and provide your response in the following format only: 'To: [recipient] with subject: [subject] and body: [body]'. provide no other commentary. make sure there are no newline characters in the answer, or just reply normally: {task}")
        
        recipient, subject, body = extract_email_details(ai_response)
        
        if recipient and subject and body:
            send_email(recipient, subject, body)
            return {"status": "Email sent", "recipient": recipient, "subject": subject, "body": body}
    elif agent_to_call == 'calendar agent' or similar(agent_to_call, available_agents[1]) > 0.9:
        ai_response = ai_chat(f"Analyze the request and provide your response in the following format only: 'Schedule an event titled: [title] on: [YYYY-MM-DD] at: [HH:MM] for: [hours] hours with: [attendees]'. provide no other commentary. make sure there are no newline characters in the answer, or just reply normally: {task}")
        title, start_time, end_time, attendees = extract_event_details(ai_response)

        if title and start_time and end_time:
            event_link = create_calendar_event(title, start_time, end_time, attendees)
            return {"status": "Event created", "link": event_link}

    
    return {"response": ai_response}

# Run with: uvicorn main:app --reload
