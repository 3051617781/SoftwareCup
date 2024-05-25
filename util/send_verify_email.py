import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import config
from util.auth_token import create_token


async def send_verify_email(receiver_email: str):
    sender_email = config.email_smtp_user
    sender_password = config.email_smtp_password

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "【智飞易写】新账号验证"

    token = create_token({"email": receiver_email})
    content = f"请点击链接验证账号：{config.backend_host}:{config.bind_port}/user/verify?token={token}"
    message.attach(MIMEText(content, "plain"))

    with smtplib.SMTP_SSL(config.email_smtp_server, config.email_smtp_port) as server:
        server.ehlo()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
