#!/usr/bin/python3
import nntplib, sys, re
from config import auth

try:
	s0 = nntplib.NNTP_SSL(host=auth[0]['server'],user=auth[0]['username'],password=auth[0]['password'])
	s1 = nntplib.NNTP_SSL(host=auth[1]['server'],user=auth[1]['username'],password=auth[1]['password'])
	s2 = nntplib.NNTP_SSL(host=auth[2]['server'],user=auth[2]['username'],password=auth[2]['password'])
	s3 = nntplib.NNTP_SSL(host=auth[3]['server'],user=auth[3]['username'],password=auth[3]['password'])
#	s4 = nntplib.NNTP_SSL(host=auth[4]['server'],user=auth[4]['username'],password=auth[4]['password'])
	s5 = nntplib.NNTP_SSL(host=auth[5]['server'],user=auth[5]['username'],password=auth[5]['password'])
except nntplib.NNTPError:
	pass

msgid_regex = re.compile('^<[^@]+@[^@]+>$')

def check_msgid(msg_id, connection, server_name):
	try:
		print(server_name)
		header = connection.head(msg_id)[1][2]
		for h in header:
			print(h.decode('utf-8'))
	except nntplib.NNTPError:
		pass

def last_header(group, connection, server_name):
	try:
		print(server_name)
		_, _, _, last, _ = connection.group(group)
		print(connection.head(last))
	except nntplib.NNTPError:
		pass

def over_last(group, connection, server_name):
	try:
		print(server_name)
		_, _, _, last, _ = connection.group(group)
		print(connection.over((last,last)))
	except nntplib.NNTPError:
		pass
		
def main():
	if re.match(msgid_regex, sys.argv[1]):
		msgid = sys.argv[1]
		check_msgid(msgid, s0, 'Highwinds')
		check_msgid(msgid, s1, 'XSNews')
		check_msgid(msgid, s2, 'Newsoo')
		check_msgid(msgid, s3, 'Astraweb')
#		check_msgid(msgid, s4, 'Supernews')
		check_msgid(msgid, s5, 'Tweaknews')
	elif len(sys.argv[1]) != 0:
		group = sys.argv[1]
		if len(sys.argv) == 2:
			last_header(group, s0, 'Highwinds')
			last_header(group, s1, 'XSNews')
			last_header(group, s2, 'Newsoo')
			last_header(group, s3, 'Astraweb')
#			last_header(group, s4, 'Supernews')
			last_header(group, s5, 'Tweaknews')
		else:
			over_last(group, s0, 'Highwinds')
			over_last(group, s1, 'XSNews')
			over_last(group, s2, 'Newsoo')
			over_last(group, s3, 'Astraweb')
#			over_last(group, s4, 'Supernews')
			over_last(group, s5, 'Tweaknews')

if __name__ == '__main__':
	main()
