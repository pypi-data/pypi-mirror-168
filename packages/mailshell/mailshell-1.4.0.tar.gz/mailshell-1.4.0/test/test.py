import os
import smtplib
import imghdr, json
from email.message import EmailMessage

d = {
	"number": None,
	"hello": "msl"
}
with open("data.json", "r") as f:
	a, b = json.load(f).values()
	print(a, b)

