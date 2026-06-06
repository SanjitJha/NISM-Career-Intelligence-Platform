"""
Emails the weekly Excel report as an attachment.
Configure EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT in .env
"""
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT, SMTP_HOST, SMTP_PORT
from reports.weekly_report import generate_report
from loguru import logger


def send_weekly_report():
    if not all([EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT]):
        logger.warning("[Email] Email credentials not configured. Skipping send.")
        return

    report_path = generate_report()

    msg = MIMEMultipart()
    msg["From"]    = EMAIL_SENDER
    msg["To"]      = EMAIL_RECIPIENT
    msg["Subject"] = "📊 NISM Career Intelligence — Weekly Report"

    body = "Hi,\n\nPlease find this week's NISM job market report attached.\n\nNISM Career Intelligence Platform"
    msg.attach(MIMEText(body, "plain"))

    with open(report_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(report_path)}")
        msg.attach(part)

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())

    logger.info(f"[Email] Report sent to {EMAIL_RECIPIENT}")

touch $BASE/reports/__init__.py
