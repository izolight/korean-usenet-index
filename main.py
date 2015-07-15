import nntplib, re
from config import auth

encoding = 'utf-8'
errors = 'ignore'

s0 = nntplib.NNTP(host=auth[0]['server'],user=auth[0]['username'],password=auth[0]['password'])
s1 = nntplib.NNTP(host=auth[1]['server'],user=auth[1]['username'],password=auth[1]['password'])
#s2 = nntplib.NNTP(host=auth[2]['server'],user=auth[2]['username'],password=auth[2]['password'])

pattern = re.compile(r"(?P<subject>.+?) \[(?P<part>\d{1,4})\/(?P<total_parts>\d{1,4})\] \- \"(?P<filename>.+?)\" yEnc \((?P<segment>\d{1,4})\/(?P<total_segments>\d{1,4})")

s0.group('korea.binaries.tv')
resp, overviews = s0.over((44100000,44100010))
subjects = {}

for number, header in overviews:
	subject, part_nr, total_parts, filename, segment_nr, total_segments = pattern.match(header['subject']).groups()
	segment = {'message-id':header['message-id'], 'bytes':header[':bytes']}
	part = {'name':filename, 'total_segments':total_segments, 'poster':header['from'], 'date':header['date'], segment_nr:segment}
	subjects[subject] = {'total_parts':total_parts, part_nr:part}
#	print(header['subject'])
#	cur_sub = re.split("\(\d{1,4}\/\d{1,4}\)",ov[1]['subject'])[0]
#	if cur_sub in subjects:
#		subjects[cur_sub] += 1
#	else:
#		subjects[cur_sub] = 1
#for s_key, s in subjects.items():
#	print('Subject %s %d' % (s_key.encode(encoding,errors).decode(encoding),s))
for s in subjects:
	print(subjects[s])

#construct for saving stuff
#{'subject':
#	{'total_parts':number, part_nr: # subject
#		{'name':filename, 'total_segments':number, 'poster':from, 'date':date, segment_nr: #part
#			{'bytes':bytes, 'message_id':message_id} # segment
#		}
#	}
#}
