import sys, os
import argparse
from . import helper
from . import mail_shell as mshell

def txt_file(f=None):
	ext = os.path.splitext(f)[1]	
	if ext == '.txt': return f
	PARSER.error(f"'{f}' is not (.txt) file!")

def main():

    # get the arguments and commands
	PARSER = argparse.ArgumentParser(prog="mailshell", description=helper.DESCRIPTION, epilog=helper.EPILOG)
	PARSER.add_argument('--version', action="store_true", help="see your current version.")

	SUBPARSER = PARSER.add_subparsers(dest="command")
	SUBPARSER.required = False

	GET_PARSER = SUBPARSER.add_parser('get', help="add a text from .txt file to you current message.")
	GET_PARSER.add_argument('file', type=txt_file, help="text file path (except .txt files)")

	ADD_PARSER = SUBPARSER.add_parser('add', help="add a file or image to your message.")
	ADD_PARSER.add_argument('file', help="file or image")

	RM_PARSER = SUBPARSER.add_parser('rm', help="remove a file or image from your message.")
	RM_PARSER.add_argument('file', nargs='?', help="the filename that has been included in the message.")
	RM_PARSER.add_argument('-a', '--all', action="store_true", help="remove all the files in the message attachments.")

	SUBPARSER.add_parser('logo', help="prints the Email logo.")
	SUBPARSER.add_parser('login', help="log in to your gmail using email address and the app password.")
	SUBPARSER.add_parser('logout', help="log out from your gmail.")
	SUBPARSER.add_parser('cred', help="print your current email address and app password.")
	SUBPARSER.add_parser('new', help="create new email message.")
	SUBPARSER.add_parser('edit', help="edit your current message.")
	SUBPARSER.add_parser('html', help="add html message.")
	SUBPARSER.add_parser('content', help="see the current message content with the included files.")
	SUBPARSER.add_parser('send', help="send the current message.")
	SUBPARSER.add_parser('to', help="set your contact that you will send to.")
	SUBPARSER.add_parser('subject', help="set a new subject to the message.")
	SUBPARSER.add_parser('from', help="set a new sender name.")
	SUBPARSER.add_parser('check', help="check your emails with a specified mailbox and search command.")
	SUBPARSER.add_parser('sch', help="print the search commands that you need for checking emails.")
	SUBPARSER.add_parser('help', help="")
	
	ARGS = PARSER.parse_args()
	if ARGS.version: 
		print("Mailshell", helper.VERSION)
		return
	try: mshell.run(ARGS)
	except KeyboardInterrupt:
		return


if __name__ == '__main__':
	main()

