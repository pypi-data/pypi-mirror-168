import sys, os
import difflib
import argparse
from . import mail_shell as msl


DESCRIPTION = "send and check emails faster from the terminal"
EPILOG = "project home page on https://github.com/malkiAbdoo/mailshell"
USAGE = "msl [COMMAND] [OPTIONS]. See 'msl --help'."

def main():

	def txt_file(f=None):
		ext = os.path.splitext(f)[1]	
		if ext == '.txt': return f
		PARSER.error(f"'{f}' is not (.txt) file!")

	def html_file(f=None):
		ext = os.path.splitext(f)[1]	
		if ext == '.html': return f
		PARSER.error(f"'{f}' is not an html file!")

	def command_check():
		if len(sys.argv) == 1: return
		cmd = sys.argv[1]
		msl_commands = msl.Mailshell().commands.keys()
		if cmd in msl_commands or cmd.startswith('-'): return
		similars = difflib.get_close_matches(cmd, msl_commands)
		msg = f"mailshell: error: '{cmd}' is not an msl command. See 'msl --help'\n"
		if not similars: PARSER.error(msg)
		msg += "Did you mean? : " + ' | '.join(similars)
		PARSER.error(msg)

	SELECTORS = [
		['-a', '--all'     , "select all the emails in the mailbox."       ],
		['-n', '--new'     , "select the recent email."                    ],
		['-s', '--subject' , "select the email which has <Subject>"        ],
		['-f', '--sender'  , "select emails that are from <sender>"        ],
		['-T', '--to'      , "select emails that were sent to <reciever>"  ],
		['-d', '--date'    , "select email that are on ' day-month-year '" ],
		['-t', '--text'    , "select email that has <TEXT>"                ]]

    # get the arguments and commands
	PARSER = argparse.ArgumentParser(prog="mailshell", description=DESCRIPTION, epilog=EPILOG, usage=USAGE)
	command_check()
	PARSER.add_argument('--version', action="store_true", help="see your current version.")

	SUBPARSER = PARSER.add_subparsers(dest="command")
	SUBPARSER.required = False

	CONTENT_PARSER = SUBPARSER.add_parser('content', help="see the current message content with the included files.")
	CONTENT_PARSER.add_argument('-f', '--files', action="store_true", help="See the files that are included in the email.")
	CONTENT_PARSER.add_argument('-i', '--images', action="store_true", help="See the included images.")

	SET_PARSER = SUBPARSER.add_parser('set', help="add a text manually or from .txt file to you current message.")
	SET_PARSER.add_argument('-f', '--file', type=txt_file, help="text file path (except .txt files)")
	
	HTML_PARSER = SUBPARSER.add_parser('html', help="add html message manually or from html file.")
	HTML_PARSER.add_argument('-f', '--file', type=html_file, help="html file path (.html)")

	ADD_PARSER = SUBPARSER.add_parser('add', help="add a file or image to your message.")
	ADD_PARSER.add_argument('file', help="file or image")

	RM_PARSER = SUBPARSER.add_parser('rm', help="remove a file or image from your message.")
	RM_PARSER.add_argument('file', nargs='?', help="the filename that has been included in the message.")
	RM_PARSER.add_argument('-a', '--all', action="store_true", help="remove all the files in the message attachments.")

	SEND_PARSER = SUBPARSER.add_parser('send', help="send the current message.")
	SEND_PARSER.add_argument('-T', '--to', help="send the email to [EMAIL ADDRESS]")

	CHECK_PARSER = SUBPARSER.add_parser('check', help="check your emails with a specified mailbox and search command.")
	CHECK_PARSER.add_argument('-b', '--box', nargs='?', default="Inbox", help="select the mailbox that you want to check (the default: %(default)s).")
	CHECK_PARSER.add_argument('-l', '--list', action="store_true", help="See the search results as a list.")

	DELETE_PARSER = SUBPARSER.add_parser('delete', help="delete emails from mailbox in your account.")
	DELETE_PARSER.add_argument('-b', '--box', default="Inbox", help="select the mailbox where you want to delete (the default: %(default)s).")

	for so, lo, h in SELECTORS:
		if so in ['-a', '-n']:
			CHECK_PARSER.add_argument(so, lo, action="store_true", help=h)
			DELETE_PARSER.add_argument(so, lo, action="store_true", help=h)
		else:
			CHECK_PARSER.add_argument(so, lo, help=h)
			DELETE_PARSER.add_argument(so, lo, help=h)

	SUBPARSER.add_parser('login', help="log in to your gmail using email address and the app password.")
	SUBPARSER.add_parser('cred', help="print your current email address and app password.")
	SUBPARSER.add_parser('new', help="create new email message.")
	SUBPARSER.add_parser('subject', help="set a new subject to the message.")
	SUBPARSER.add_parser('from', help="set a new sender name.")
	SUBPARSER.add_parser('to', help="set your contact that you will send to.")
	SUBPARSER.add_parser('logout', help="log out from your gmail.")
	SUBPARSER.add_parser('help', help="mailshell helper.")

	ARGS = PARSER.parse_args()

	try: msl.run(ARGS)
	except KeyboardInterrupt:
		return


if __name__ == '__main__':
	main()

