import os
import base64
import html2text
import imaplib, email


PARTS = "(RFC822)"
IMAP_SERVER = "imap.gmail.com"
LINE = f"\x1b[33m{'-' * 50}\x1b[0m"

def mailbox_error(box):
	print(f"\nERROR: [{box}]: mailbox does not exist!. Use 'msl check -lb' to see your mailboxes.\n")

def criteria_error(cri):	
	print(f"\nERROR: No search command: you didn't add a selector. Use 'msl ckeck -h' to see the selection commands.\n")

def html_text_content(html):
	h = html2text.HTML2Text()
	h.ignore_links = True
	text = (h.handle(f'''{html}''').replace("\\r\\n", ""))
	text = text.replace("'", "")
	return text

def base64_to_utf8(string, html=False):
	try: 
		string = base64.b64decode(string.encode("utf8")).decode("utf8")
		if html: string = ""
	except: pass
	return string

def select_mailbox(client, box):
	if not box or box == "Inbox": return "Inbox"
	for mb in client.list()[1]:
		mb = mb.decode().split(' "/" ')
		if box.title() in mb[1]:
			return mb[1]
	return

def generate_criteria(args):
	cri = ""
	if args.all: cri += 'ALL'
	if args.new: cri += 'RECENT'
	if args.subject: cri += f'SUBJECT "{args.subject}"'
	if args.sender: cri += f'FROM "{args.sender}"'
	if args.to: cri += f'TO "{args.to}"'
	if args.date: cri += f'ON {args.date.title()}'
	if args.text: cri += f'TEXT "{args.text}"'
	return cri

def check(user, arg):

	print("Connecting..")
	with imaplib.IMAP4_SSL(IMAP_SERVER) as imap:
		imap.login(user.address, user.app_password)
		box = select_mailbox(imap, arg.box)
		if not box:
			mailbox_error(arg.box)
			return

		imap.select(box)
		CRI = generate_criteria(arg)

		if arg.list and box == "Inbox" and not CRI:
			print("Mailboxes list:")
			for mb in imap.list()[1]: print('\t' + mb.decode().split(' "/" ')[1])
			return
		try:
			_, msgnums = imap.search(None, CRI)
		except Exception:
			criteria_error(CRI)
			return
		if not msgnums[0]:
			print(f"No search results in [{arg.box}].")
			return
		for num in msgnums[0].split():
			_, data = imap.fetch(num, PARTS)
			message = email.message_from_bytes(data[0][1])

			subject = base64_to_utf8(message.get('Subject'))
			sender = message.get('From')
			to = message.get('To')
			date = message.get('Date')
			if arg.list:
				print(f" [Subject: {subject}] [From: {sender}] [Date: {date}]")
				continue

			print("\nSubject:\t".expandtabs(11), subject)
			print("From:\t".expandtabs(11), sender)
			print("To:\t".expandtabs(11), to)
			print("Date:\t".expandtabs(11), date)
			body = ""
			attachments = []
			if message.is_multipart():
				for part in message.get_payload():
					ctype = part.get_content_type()
					cdispo = str(part.get('Content-Disposition'))
					if ctype == 'text/plain':
						body += '\n' + base64_to_utf8(part.get_payload())
					elif ctype == "multipart/alternative" or "html" in ctype:
						if type(part.get_payload()) != str: part = part.get_payload()[1]
						body += '\n' + base64_to_utf8(html_text_content(part.get_payload()), True)
					elif 'attachment' in cdispo:
						attachments.append('\t' + part.get_filename())
				if attachments: body += '\nincludes:\n' + '\n'.join(attachments)
			else:
				body += message.get_payload(decode=False)
			print('', body, LINE, sep='\n')

def delete(user, arg):
	
	print("Connecting..")
	with imaplib.IMAP4_SSL(IMAP_SERVER) as imap:
		imap.login(user.address, user.app_password)
		box = select_mailbox(imap, arg.box)
		if not box:
			mailbox_error(arg.box)
			return
			
		imap.select(box)
		CRI = generate_criteria(arg)
		try:
			_, msgnums = imap.search(None, CRI)
		except Exception:
			criteria_error(CRI)
			return
		if not msgnums[0]:
			print(f"No search results in [{arg.box}].")
			return
		print(f"Deleting selected mails from {box}:")
		count = 0
		for mail in msgnums[0].split():
			# mark the mail as deleted
			imap.store(mail, "+FLAGS", "\\Deleted")

			_, data = imap.fetch(mail, PARTS)
			message = email.message_from_bytes(data[0][1])
			print(f"  email[Subj: {base64_to_utf(message.get('Subject'))}] [From: {message.get('From')}]", "is deleted.")

			count += 1
		print(count, f"selected email{'s have' if count > 1 else ' has'} been deleted.\n")

