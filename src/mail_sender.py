import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


async def send_email(sender_email, sender_password, recipient_email, subject, message):
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        await aiosmtplib.send(
            msg.as_string(),
            hostname=smtp_server,
            sender=sender_email,
            recipients=[recipient_email],
            port=smtp_port,
            start_tls=True,
            username=sender_email,
            password=sender_password
        )

    except Exception as e:
        print(f"Помилка при відправці email: {e}")
