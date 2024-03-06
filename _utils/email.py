from email.message import EmailMessage
import ssl
import smtplib

def send_email(subject, body, reciever):
    sender = "propertypantry@gmail.com"
    password = "Password"

    email = EmailMessage()
    email["From"] = sender
    email["To"] = reciever
    email["Subject"] = subject
    email.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, reciever, email.as_string())