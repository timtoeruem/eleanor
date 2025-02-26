import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = "timtoeruem@gmail.com"
SENDER_PASSWORD = "rjmo wfol vkiq irgk"  # Use App Password for security

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

    print(f"Email sent to {to_email}")



#if this file is executed directly test the "send_mail" function
if __name__ == "__main__":
    send_email("timtoeruem@gmail.com", "Test Subject", "Hello, this is a test email.")