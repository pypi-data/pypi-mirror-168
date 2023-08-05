import sys, os
import requests
from . import helper
import sqlite3 as sql
from . import email_logo
import smtplib, socket
import csv, re, imghdr
from pathlib import Path
from os.path import exists
from os.path import basename
from getpass import getuser
from subprocess import call
from . import mail_checker as mc
from email.message import EmailMessage
from tempfile import NamedTemporaryFile


PORT = 465
SMTP_SERVER = "smtp.gmail.com"
CREDENTIALS_FILE = (Path(__file__).parent / "credentials.csv")
DATABASE = (Path(__file__).parent / "user_data.db")
HTML_FILE = (Path(__file__).parent / "html_message.html")
MESSAGE_STR = " Your message ".center(14 + 22 * 2, '=')
EMAIL_PATTERN = r"^\s*[\w\._%+-]+@[\w\.-]+\.\w+\s*$"
SEND_TO_STR = r"//↓↓↓↓ Send to ↓↓↓↓\\"

def connect_to_database():
	if not exists(DATABASE): return
	with sql.connect(DATABASE) as data:
		c = data.cursor()
		c.execute("CREATE TABLE IF NOT EXISTS message (subject, sender, text)")
		c.execute("CREATE TABLE IF NOT EXISTS contacts (emails)")
		c.execute("CREATE TABLE IF NOT EXISTS attachments (file)")
		c.execute("INSERT INTO message VALUES (?, ?, ?)", ('', '', ""))
		c.execute("INSERT INTO contacts VALUES (?)", ('{}',))
		data.commit()

def set_user_credentials(address, pwd):
	with open(CREDENTIALS_FILE, 'w') as f:
		file_writer = csv.writer(f)
		file_writer.writerow([address, pwd])

def user_message(mode, subject=None, sender=None, message=None):
	with sql.connect(DATABASE) as data:
		c = data.cursor()
		if mode == 'GET':
			c.execute("SELECT * FROM message")
			text = c.fetchone()
			data.commit()
			return text
		if subject: c.execute("UPDATE message SET subject = ?", (subject,))
		if sender: c.execute("UPDATE message SET sender = ?", (sender,))
		if message is not None: c.execute("UPDATE message SET text = ?", (message,))
		data.commit()

def user_contacts(mode, emails=""):
	with sql.connect(DATABASE) as data:
		c = data.cursor()
		if mode == 'GET':
			c.execute("SELECT emails FROM contacts")
			contacts = eval(c.fetchone()[0])
			data.commit()
			return contacts
		c.execute("UPDATE contacts SET emails = ?", (emails,))
		data.commit()

def html_message(mode, html=""):
	if mode == 'GET':
		if not exists(HTML_FILE): return
		with open(HTML_FILE, 'r') as f:
			return f.read()
	with open(HTML_FILE, 'w') as f:
		f.write(html)

def message_attachments(mode, filename=""):
	with sql.connect(DATABASE) as data:
		c = data.cursor()
		if mode == 'GET':
			c.execute("SELECT file FROM attachments")
			attachments = list(map(lambda x: x[0], c.fetchall()))
			data.commit()
			return attachments
		if mode == 'POST':
			c.execute("INSERT INTO attachments VALUES (?)", (filename,))
		else:
			if filename[-1] == '*':
				c.execute("DELETE FROM attachments")
				return "all files are removed from the message."
			c.execute("SELECT file FROM attachments WHERE file = ?", (filename,))
			if not c.fetchone(): 
				data.commit()
				return f"ERROR: '{filename}' is not in your message."
			c.execute("DELETE FROM attachments WHERE file = ?", (filename,))
			data.commit()
			return basename(filename) + " is removed."
		data.commit()

def update_warning():
	response = requests.get("https://pypi.org/pypi/mailshell/json")
	current_version = response.json()['info']['version']
	if helper.VERSION == current_version:
		return ''
	warning = f"\n\x1b[33mWARNING: new version available [{current_version}]\n"
	warning += "run 'pip3 install -U mailshell' to update.\x1b[0m"
	return warning

def validate_email(address):
	response = requests.get('https://isitarealemail.com/api/email/validate', params={ 'email': address })
	status = response.json()['status']
	if status == "valid": 
		return True
	return False

def dispaly_logo():
	print(email_logo.LOGO)

def helpme():
	call(['mshell', '--help'])

def less(text=''):
	with NamedTemporaryFile(mode='w') as tmp:
		tmp.write(text + "\nPress 'q' to END")
		tmp.flush()
		os.fsync(tmp.fileno())
		call(['less', '-X', tmp.name])
	

class User(object):
	def __init__(self, address=None, password=None):
		self.address = address
		self.app_password = password

	def get_user(self):
		if not exists(CREDENTIALS_FILE): return
		with open(CREDENTIALS_FILE, 'r') as f:
			credentials = next(csv.reader(f))
		self.address, self.app_password = credentials

	def __bool__(self):
		return bool(self.address)

class Mailshell():
	def __init__(self):
		self.commands = {
			"logo": dispaly_logo,
			"login": self.log_in,
			"logout": self.log_out,
			"cred": self.credentials,
			"new": self.new_message,
			"edit": self.edit_message,
			"html": self.add_html,
			"content": self.show_content,
			"send": self.send_message,
			"to": self.message_to,
			"subject": self.set_subject,
			"from": self.set_from,
			"get": self.get_text,
			"add": self.add_file,
			"rm": self.remove_file,
			"check": self.check_mail_box,
			"sch": self.display_sc,
			"help": helpme
		}

	def __error_login_first(self):
		print("\nLogin first: type 'msl login' to start create and send your massages.\n")

	def __error_app_password(self):
		print(
			"\nERROR: Gmail app password is incorrect:\nsee how to create and use gmail app password on:" + 
			"\n\t\x1b[33mhttps://support.google.com/accounts/answer/185833?hl=en#app-passwords\x1b[0m\n")

	def __error_create_message(self):
		print("\nYou didn't create a message: type 'msl new' to create a new massage..\n")
	
	def __error_file_not_found(self, filename):
		print(f"\nERROR: '{filename}' does not exists.\n")

	def __error_connection(self):
		print("\nConnection error: please check your network!\n")
	
	def __has_message(self):
		subj = user_message('GET')[0]
		if subj: return True
		self.__error_create_message()
		return False

	def __has_user(self):
		user = User()
		user.get_user()
		if user: return True
		self.__error_login_first()
		return False
		
	def __get_multiline_input(self, prefix='', strp=False):
		with NamedTemporaryFile(mode='w') as f:
			f.write(prefix)
			f.flush()
			os.fsync(f.fileno())
			with open(f.name, 'r') as tmp:
				call(['nano', tmp.name])
				text = tmp.read()
				if strp: text = text.strip()
				return text

	def log_in(self):
		print('\nLog in:')
		address = input("Email address: ").strip()
		password = input("App password: ").strip()
		try:
			if validate_email(address):
				try:
					with smtplib.SMTP_SSL(SMTP_SERVER, PORT) as smtp:
						smtp.login(address, password)
				except smtplib.SMTPAuthenticationError:
					self.__error_app_password()
					return
			else:
				print(f"ERROR: '{address}' does not exist.\n")
				return
			print(update_warning())
		except Exception:
			self.__error_connection()
			return

		set_user_credentials(address, password)
		print("\x1b[32mYou have been successfully logged in.\x1b[0m\n")

	def log_out(self):
		if not self.__has_user(): return
		os.remove(CREDENTIALS_FILE)
		print("\nYou have logged out.\n")

	def credentials(self):
		user = User()
		user.get_user()
		if not user:
			self.__error_login_first()
			return
		print("\nEmail address:\t" + user.address)
		print("Email app password:\t" + user.app_password, '\n')

	def new_message(self):
		if not self.__has_user(): return
		print("\nCreating new message:")
		self.set_subject(True)
		self.set_from(True)
		user_message('POST', message="")
		message_attachments('DELETE', '*')
		try: os.remove(HTML_FILE)
		except: pass

	def edit_message(self):
		subj, _, content = user_message('GET')
		if not subj:
			self.__error_create_message()
			return
		new_content = self.__get_multiline_input(content)
		user_message('POST', message=new_content)

	def add_html(self):
		if not self.__has_message(): return
		new = self.__get_multiline_input(html_message('GET') or "", True)
		if new: html_message('POST', html=new)
		try: os.remove(HTML_FILE)
		except: pass

	def set_subject(self, allowed=False):
		subj = user_message('GET')[0]
		if not allowed and not subj:
			self.__error_create_message()
			return
		while True:
			subj = input("Subject: ").strip()
			if subj:
				user_message('POST', subject=subj)
				break
			print("You have to set a Subject to your message!")

	def set_from(self, allowed=False):
		user = User()
		user.get_user()
		subj = user_message('GET')[0]
		if not allowed and not subj:
			self.__error_create_message()
			return
		sdr = input("From: ").strip()
		if sdr: sdr += ' '
		sdr += f"<{user.address}>"
		user_message('POST', sender=sdr)
	
	def get_text(self, file_path=''):
		subj, _, content = user_message('GET')
		if not subj:
			self.__error_create_message()
			return
		if not exists(file_path):
			self.__error_file_not_found(file_path)
			return
		with open(file_path, 'r') as f:
			content += f.read()
			user_message('POST', message=content)

	def add_file(self, file_path=''):
		if not self.__has_message(): return
		if not exists(file_path):
			self.__error_file_not_found(file_path)
			return
		if os.path.isdir(file_path):
			print(f"\n{file_path} is a folder not file.\n")
			return
		message_attachments('POST', os.path.abspath(file_path))
					

	def remove_file(self, filename=''):
		print(message_attachments('DELETE', os.path.abspath(filename)))

	def show_content(self):
		if not self.__has_message(): return
		line = '-' * len(MESSAGE_STR)
		content = MESSAGE_STR + '\n'
		subject, sender, text = user_message('GET')
		content += f"Subject:\t{subject}\n" + f"From:\t{sender}\n"
		if exists(HTML_FILE): text = html_message('GET')
		content += text + '\n'
		attachments = message_attachments('GET')
		if attachments:
			content += line + "\n- includes:\n"
			for att in attachments: content += f"\x1b[33m\t{basename(att)}\x1b[0m\n" 
		print(content, '\n' + line)
		print("type 'send' to send your message.\n")

	def check_mail_box(self):
		user = User()
		user.get_user()
		if not user:
			self.__error_login_first()
			return
		try:
			mc.check(user)
			print(update_warning())
		except socket.gaierror:
			self.__error_connection()

	def display_sc(self):
		less(helper.IMAP_CRITERIAS)

	def message_to(self):
		if not self.__has_user(): return
		pre = SEND_TO_STR + '\n' + '\n'.join(list(user_contacts('GET')))
		result = self.__get_multiline_input(pre)
		matches = re.findall(EMAIL_PATTERN, result, re.MULTILINE)
		contacts = set(map(lambda x: x.strip(), matches))
		user_contacts('POST', str(contacts))
		return contacts
		  
	def send_message(self):
		user = User()
		user.get_user()
		subject, sender, text = user_message('GET')
		if not subject:
			self.__error_create_message()
			return
		contacts = self.message_to()
		if not contacts:
			print("You have no receivers: type 'msl to' to set your contacts.")
			return
		try:
			print("\nConnecting..")
			with smtplib.SMTP_SSL(SMTP_SERVER, PORT) as smtp:
				smtp.login(user.address, user.app_password)
				message = EmailMessage()
				message['Subject'] = subject
				message['From'] = sender
				message.set_content(text)
				if exists(HTML_FILE):
					message.add_alternative(html_message('GET'), subtype='html')
				for att in message_attachments('GET'):
					if imghdr.what(att):
						mtype, stype = 'image', imghdr.what(att)
					else:
						mtype, stype = 'application', 'octet-stream'

					with open(att, 'rb') as f:
						message.add_attachment(
        					f.read(),
        					maintype=mtype,
        					subtype=stype,
        					filename=basename(f.name)
    					)
				for user in contacts:
					print(f"Sending to {user}..")
					if not validate_email(user):
						print(f"\x1b[31m    Error: {user} is not exist.\x1b[0m")
						continue
					message['To'] = user
					smtp.send_message(message)
					print("\x1b[32m    Email is successfully sent\x1b[0m")
			print(update_warning())
		except socket.gaierror:
			self.__error_connection()
	def __getitem__(self, args):
		cmd, f = args
		if cmd in self.commands:
			connect_to_database()
			if f: self.commands[cmd](f)
			else: self.commands[cmd]()
			return
		print(f"'{cmd}' command not found.")
		


def run(arguments=None):
	SHELL = Mailshell()
	if not arguments.command:
		helpme()
		return
	try: command = [arguments.command, arguments.file]
	except AttributeError: command = [arguments.command, None]
	if command[0] == "rm" and arguments.all: command[1] = "*"
	SHELL[command]

