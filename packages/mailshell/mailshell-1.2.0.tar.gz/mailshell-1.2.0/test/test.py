
import os
import smtplib
import imghdr
from email.message import EmailMessage

EMAIL_ADDRESS = "malkiabderahman@gmail.com"
EMAIL_PASSWORD = "zvazugsqztteumvi"

msg = EmailMessage()
msg['Subject'] = 'send html mail'
msg['From'] = EMAIL_ADDRESS
msg['To'] = "abdo.malkiep@gmail.com"

msg.set_content('This is a plain text email')

msg.add_alternative("""\
<!DOCTYPE html>
<html>
    <body>
        <h1 style="color:SlateGray;">This is an HTML Email!</h1>
    </body>
</html>
""", subtype='html')
del msg.get_payload()[1]
msg.add_alternative("""\
<!DOCTYPE html>
<html>
    <body>
        <h1 style="color:SlateGray;">Hello!</h1>
    </body>
</html>
""", subtype='html')

for att in msg.get_payload():
	if att.get_content_subtype() == "html": print(att.get_content())


#with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
#    smtp.send_message(msg)

