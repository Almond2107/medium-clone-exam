import smtplib
from email.mime.text import MIMEText
from app.settings import SMTP_SERVER, SMTP_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD
from app.tasks import celery_app

@celery_app.task
def send_verification_email(to_email: str, token: str):
    subject = "Verify your email"
    verify_link = f"http://localhost:8000/auth/verify-email/{token}"
    body = f"Click this link to verify your email: {verify_link}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
