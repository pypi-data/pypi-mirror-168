import os
import html2text
import imaplib, email


def html_text_content(html):
	h = html2text.HTML2Text()
	h.ignore_links = True
	text = (h.handle(f'''{html}''').replace("\\r\\n", ""))
	text = text.replace("'", "")
	return text


def check(user=None):
	IMAP_SERVER = "imap.gmail.com"

	print("Connecting..")
	with imaplib.IMAP4_SSL(IMAP_SERVER) as imap:
		#imap.login(user.address, user.app_password)
		imap.login("app.mailshell@gmail.com", "ghpdruxkraabdppl")
		box = input("mailbox: ").strip().title()
		if not box: box = 'Inbox'
		for b in imap.list()[1]:
			if box == 'Inbox': break
			b = b.decode().split(' "/" ')
			if box in b[1]:
				box = b[1]
				break
		else:
			print("This box does not exist!")
			return

		imap.select(box)
		CRI = input("Search command: ").strip()
		try:
			_, msgnums = imap.search(None, CRI)
		except Exception:
			print("\nInvalid command: type 'sch' to see the email search commands.\n")
			return
		if not msgnums[0]:
			print("No search results in this mail box.")
			return
		for num in msgnums[0].split():
			_, data = imap.fetch(num, "(RFC822)")
			message = email.message_from_bytes(data[0][1])
			print("\nSubject:\t", message.get('Subject'))
			print("From:\t", message.get('From'))
			print("To:\t", message.get('To'))
			print("Date:\t", message.get('Date'))
			body = ""
			attachments = []
			if message.is_multipart():
				for part in message.get_payload():
					ctype = part.get_content_type()
					cdispo = str(part.get('Content-Disposition'))
					if ctype == 'text/plain':
						body += '\n' + part.get_payload()
					elif ctype == "multipart/alternative" or "html" in ctype:
						if type(part.get_payload()) != str: part = part.get_payload()[1]
						body += '\n' + html_text_content(part.get_payload())
					elif 'attachment' in cdispo:
						attachments.append('\t' + part.get_filename())
				if attachments: body += '\nincludes:\n' + '\n'.join(attachments)
			else:
				body += message.get_payload(decode=False)
			print("\n" + body)
			print(f"\x1b[33m{'-' * 50}\x1b[0m")

