#!/usr/bin/python3
import nntplib, sys, re
from config import auth

s0 = nntplib.NNTP_SSL(host=auth[0]['server'],user=auth[0]['username'],password=auth[0]['password'])
s1 = nntplib.NNTP_SSL(host=auth[1]['server'],user=auth[1]['username'],password=auth[1]['password'])
s2 = nntplib.NNTP_SSL(host=auth[2]['server'],user=auth[2]['username'],password=auth[2]['password'])
s3 = nntplib.NNTP_SSL(host=auth[3]['server'],user=auth[3]['username'],password=auth[3]['password'])

msgid_regex = re.compile('^<[^@]+@[^@]+>$')

def check_msgid(msg_id, connection, server_name):
	try:
		print(server_name)
		header = connection.head(msg_id)[1][2]
		for h in header:
			print(h.decode('utf-8'))
	except nntplib.NNTPTemporaryError:
		pass

def last_header(group, connection, server_name):
	try:
		print(server_name)
		_, _, _, last, _ = connection.group(group)
		print(connection.head(last))
	except nntplib.NNTPTemporaryError:
		pass
		
def main():
	if re.match(msgid_regex, sys.argv[1]):
		msgid = sys.argv[1]
		check_msgid(msgid, s0, 'Highwinds')
		check_msgid(msgid, s1, 'XSNews')
		check_msgid(msgid, s2, 'Newsoo')
		check_msgid(msgid, s3, 'Astraweb')
	elif len(sys.argv[1]) != 0:
		group = sys.argv[1]
		last_header(group, s0, 'Highwinds')
		last_header(group, s1, 'XSNews')
		last_header(group, s2, 'Newsoo')
		last_header(group, s3, 'Astraweb')


if __name__ == '__main__':
	main()
