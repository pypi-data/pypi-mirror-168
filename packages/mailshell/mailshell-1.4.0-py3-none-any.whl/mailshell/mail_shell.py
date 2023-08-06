import sys, os
import requests
from . import helper
import smtplib, socket
import json, re, imghdr
from pathlib import Path
from os.path import exists
from os.path import basename
from getpass import getuser
from subprocess import call
from . import email_checker as mc
from email.message import EmailMessage
from tempfile import NamedTemporaryFile


PORT = 465
SMTP_SERVER = "smtp.gmail.com"
USER_DATA = (Path(__file__).parent / "msl-user.json")
HTML_FILE = (Path(__file__).parent / "html_message.html")
MESSAGE_STR = " Your message ".center(14 + 22 * 2, '=')
EMAIL_PATTERN = r"^\s*[\w\._%+-]+@[\w\.-]+\.\w+\s*$"
SEND_TO_STR = r"//↓↓↓↓ Send to ↓↓↓↓\\"

def connect_to_data():
	if exists(USER_DATA): return
	with open(USER_DATA, 'w') as data:
		json.dump(
		{
			"credentials": {
				"address": None,
				"password": None
			},
			"message": {
				"subject": "",
				"from": "",
				"text": "",
				"attachments": []
			},
			"contacts": []
		},
		data, indent=2)

def user_data(mode, obj=None):
	if mode == 'GET':
		with open(USER_DATA) as data:
			return json.load(data)
	with open(USER_DATA, 'w') as data:
		json.dump(obj, data, indent=2)

def html_message(mode):
	if mode == 'GET':
		if not exists(HTML_FILE): return
		with open(HTML_FILE, 'r') as f:
			return f.read().strip()
	call(['nano', HTML_FILE])
	with open(HTML_FILE, 'r') as html:
		if not html.read().strip(): os.remove(HTML_FILE)

def update_warning():
	response = requests.get("https://pypi.org/pypi/mailshell/json")
	current_version = response.json()['info']['version']
	if helper.VERSION == current_version:
		return ""
	warning = f"\n\x1b[33mWARNING: new version available [{current_version}]\n"
	warning += "See 'pip3 install -U mailshell' to update.\x1b[0m\n"
	return warning

def validate_email(address):
	response = requests.get('https://isitarealemail.com/api/email/validate', params={ 'email': address })
	status = response.json()['status']
	if status == "valid": 
		return True
	return False

def helpme():
	call(['msl', '--help'])

def show(text=''):
	lines = os.get_terminal_size()[1]
	if len(text.splitlines()) <= lines - 2:
		print(text)
		return
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
		cred = user_data('GET')["credentials"].values()
		self.address, self.app_password = cred

	def __bool__(self):
		return bool(self.address)

class Mailshell():
	def __init__(self):
		self.commands = {
			"login": self.log_in,
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
			"help": helpme,
			"logout": self.log_out
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
		subj = user_data('GET')["message"]["subject"]
		if subj: return True
		self.__error_create_message()
		return False

	def __has_user(self):
		if user_data('GET')["credentials"]["address"]: return True
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
		address = input("> Email address: ").strip()
		password = input("> App password: ").strip()
		try:
			if validate_email(address):
				try:
					with smtplib.SMTP_SSL(SMTP_SERVER, PORT) as smtp:
						smtp.login(address, password)
				except smtplib.SMTPAuthenticationError:
					self.__error_app_password()
					return
			else:
				print(f"\nERROR: '{address}' does not exist.\n")
				return
			print(update_warning())
		except Exception:
			self.__error_connection()
			return
		
		data = user_data('GET')
		data["credentials"]["address"] = address
		data["credentials"]["password"] = password
		user_data('POST', data)

		print("\x1b[32mYou have been successfully logged in.\x1b[0m\n")

	def log_out(self):
		if not self.__has_user(): return
		os.remove(USER_DATA)
		print("\nYou have logged out.\n")

	def credentials(self):
		user = User()
		user.get_user()
		if not user:
			self.__error_login_first()
			return
		print("\nEmail address:       " + user.address)
		print("Email app password:  " + user.app_password, '\n')

	def new_message(self):
		if not self.__has_user(): return
		print("\nCreating new message:")
		data = user_data('GET')
		data["message"]["subject"] = self.set_subject(True) 
		data["message"]["from"] = self.set_from(True)
		data["message"]["text"] = ""
		data["message"]["attachments"] = []
		user_data('POST', data)
		try: os.remove(HTML_FILE)
		except: pass

	def edit_message(self):
		data = user_data('GET')
		if not data["message"]["subject"]:
			self.__error_create_message()
			return
		data["message"]["text"] = self.__get_multiline_input(data["message"]["text"])
		user_data('POST', data)

	def add_html(self):
		if not self.__has_message(): return
		html_message('POST')

	def set_subject(self, allowed=False):
		data = user_data('GET')
		subj = data["message"]["subject"]
		if not allowed:
			if not subj:
				self.__error_create_message()
				return
			print("your current message subject is:", subj, "\nset a new one:")
		while True:
			subj = input("> Subject: ").strip()
			if subj:
				if allowed: return subj
				data["message"]["subject"] = subj
				user_data('POST', data)
				break
			print("You have to set a Subject to your message!")

	def set_from(self, allowed=False):
		data = user_data('GET')
		sdr = data["message"]["from"]
		if not allowed:
			if not data["message"]["subject"]:
				self.__error_create_message()
				return
			print("This message is from: ", sdr, "\nset a new name:")
		sdr = input("> From: ").strip()
		if sdr: sdr += ' '
		sdr += f"<{data['credentials']['address']}>"
		if allowed: return sdr
		data["message"]["from"] = sdr
		user_data('POST', data)
	
	def get_text(self, file_path=''):
		data = user_data('GET')
		if not data["message"]["subject"]:
			self.__error_create_message()
			return
		if not exists(file_path):
			self.__error_file_not_found(file_path)
			return
		with open(file_path, 'r') as f:
			data["message"]["text"] += f.read()
			user_data('POST', data)

	def add_file(self, file_path=''):
		if not self.__has_message(): return
		data = user_data('GET')
		if not exists(file_path):
			self.__error_file_not_found(file_path)
			return
		if os.path.isdir(file_path):
			print(f"\n'{file_path}' is a folder not file.\n")
			return
		data["message"]["attachments"].append(os.path.abspath(file_path))
		user_data('POST', data)

	def remove_file(self, filename=''):
		if not self.__has_message(): return
		data = user_data('GET')
		if filename == '*':
			data["message"]["attachments"] = []
			user_data('POST', data)
			print("all files are removed from the message.")
			return 
		try:
			data["message"]["attachments"].remove(os.path.abspath(filename))
			user_data('POST', data)
			print(basename(filename), "is removed.")
		except ValueError: print(f"ERROR: '{filename}' is not in your message.")

	def show_content(self):
		data = user_data('GET')
		if not data["message"]["subject"]:
			self.__error_create_message()
			return
		line = '-' * len(MESSAGE_STR)
		content = '\n' + MESSAGE_STR + '\n'
		subject, sender, text, attachments = data["message"].values()
		content += f"Subject:  {subject}\nFrom:     {sender}\n"
		if exists(HTML_FILE): text = html_message('GET')
		content += f"\n{text}\n"
		if attachments:
			content += line + "\n- includes:"
			for att in attachments: content += f"\n\x1b[33m\t{basename(att)}\x1b[0m" 
		show(content + '\n' + line)
		print("Use 'msl send' to send your message.\n")

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
		show(helper.IMAP_CRITERIAS)

	def message_to(self):
		if not self.__has_user(): return
		data = user_data('GET')
		pre = SEND_TO_STR + '\n' + '\n'.join(data["contacts"])
		result = self.__get_multiline_input(pre)
		matches = re.findall(EMAIL_PATTERN, result, re.MULTILINE)
		contacts = list(set(map(lambda x: x.strip(), matches)))
		data["contacts"] = contacts
		user_data('POST', data)
		return contacts
		  
	def send_message(self):
		user = User()
		user.get_user()
		data = user_data('GET')
		subject, sender, text, attachments = data["message"].values()
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
				if exists(HTML_FILE): message.add_alternative(html_message('GET'), subtype='html')
				for att in attachments:
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
						print(f"\t\x1b[31mError: {user} does not exist.\x1b[0m")
						continue
					message['To'] = user
					smtp.send_message(message)
					print("\t\x1b[32mEmail is successfully sent\x1b[0m")
			print(update_warning())
		except socket.gaierror:
			self.__error_connection()
	def __getitem__(self, args):
		cmd, f = args
		if cmd in self.commands:
			connect_to_data()
			if f: self.commands[cmd](f)
			else: self.commands[cmd]()
		


def run(arg=None):
	SHELL = Mailshell()
	if not arg.command:
		if arg.version: print("Mailshell", f"[ {helper.VERSION} ]")
		else: helpme()
		return

	try: command = [arg.command, arg.file]
	except AttributeError: command = [arg.command, None]
	if command[0] == "rm" and arg.all: command[1] = "*"
	SHELL[command]

