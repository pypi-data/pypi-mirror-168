import datetime
import json
import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from hareqres.jwtbearer import encode_jwt, decode_jwt
from jinja2 import Template


from hareqres.jwtbearer import JWT_SECRET, JWT_ALGORITHM
from hareqres.user import User
from hadata.user import MongoUser
from hautils.logger import logger


def email_token(receiver):
    logger.info("email token called with %s" % (receiver,))
    payload = {
        "email": receiver,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=2)
    }
    logger.info("token creation %s" % (payload,))
    token = encode_jwt(payload)
    logger.info("token created %s" % (token,))
    return token


def send_email(receiver):
    logger.info("called send email with %s" % (receiver,))
    sender = "noreply@hiacuity.com"
    report_file = open(Path("templates/email.html"))
    template = Template(report_file.read())

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "HiAcuity Account Verification"
    msg['From'] = sender
    msg['To'] = receiver

    token = email_token(receiver)

    text = "Thank you for registering with HiAcuity!" + \
           "\nCopy and paste the following link on a browser window to activate your account.:" + \
           "\nhttps://dev.hiacuity.com/verify/" + token
    html = template.render(token=token)

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    s = smtplib.SMTP_SSL('email-smtp.ap-southeast-1.amazonaws.com', 465)
    s.ehlo()
    s.login("AKIA5CLBR5JUUQRFHA77", "BJz4vVxAAU4gM9oRba3z2ccnKAMjG7+yXbpOi0y6COYp")
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()


async def send_email_2(receiver, instance: User):
    logger.info("called send email 2 with %s" % (receiver,))
    sender = "noreply@hiacuity.com"
    report_file = open(Path("templates/email_2.html"))
    template = Template(report_file.read())

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "HiAcuity Account Verification"
    msg['From'] = sender
    msg['To'] = receiver

    token = email_token(receiver)

    text = "Hi" + instance[
        'first_name'] + "\nYou have been invited!. Below you will find your account password and also the link to verify your account." + \
           "\nTemporary password:" + instance[
               'password'] + "\nCopy and paste the following link on a browser window to activate your account." + \
           "\nhttps://dev.hiacuity.com/verify/" + token + "/" + instance['email'] + "/" + instance['first_name'] + "/" + \
           instance['last_name']

    html = template.render(token=token,
                           password=instance['password_string'],
                           first_name=instance['first_name'],
                           last_name=instance['last_name'],
                           email=instance['email'])

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    s = smtplib.SMTP_SSL('email-smtp.ap-southeast-1.amazonaws.com', 465)
    s.ehlo()
    s.login("AKIA5CLBR5JUUQRFHA77", "BJz4vVxAAU4gM9oRba3z2ccnKAMjG7+yXbpOi0y6COYp")
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()


