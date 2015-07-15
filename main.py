import nntplib, re
from config import auth

encoding = 'utf-8'
errors = 'ignore'

s0 = nntplib.NNTP(host=auth[0]['server'],user=auth[0]['username'],password=auth[0]['password'])
s1 = nntplib.NNTP(host=auth[1]['server'],user=auth[1]['username'],password=auth[1]['password'])
#s2 = nntplib.NNTP(host=auth[2]['server'],user=auth[2]['username'],password=auth[2]['password'])

s0.group('korea.binaries.tv')
resp, overviews = s0.over((44100000,44100010))
subjects = {}
for number, header in overviews:
	subject, part, total_parts, filename, segement, total_segements =  re.match(r"(.*) \[(\d{1,4})\/(\d{1,4})\] \- \"(.*)\" yEnc \((\d{1,4})\/(\d{1,4})", header['subject']).groups()
	print(subject)
#	print(header['subject'])
#	cur_sub = re.split("\(\d{1,4}\/\d{1,4}\)",ov[1]['subject'])[0]
#	if cur_sub in subjects:
#		subjects[cur_sub] += 1
#	else:
#		subjects[cur_sub] = 1
#for s_key, s in subjects.items():
#	print('Subject %s %d' % (s_key.encode(encoding,errors).decode(encoding),s))
