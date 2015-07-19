#! /usr/bin/python3
import nntplib, re
from config import auth
from time import time

encoding = 'utf-8'
errors = 'ignore'

s0 = nntplib.NNTP(host=auth[0]['server'],user=auth[0]['username'],password=auth[0]['password'])

pattern = re.compile(r"(?P<subject>.+?) \[(?P<part>\d{1,4})\/(?P<total_parts>\d{1,4})\] \- \"(?P<filename>.+?)\" yEnc \((?P<segment>\d{1,4})\/(?P<total_segments>\d{1,4})")

n_headers = 50000
resp, count ,first, last, name = s0.group('korea.binaries.tv')
t0 = time()
resp, overviews = s0.over((last-n_headers,last))
t1 = time()
print('got %s headers in %f seconds' % (n_headers,(t1-t0)))
subjects = {}

for number, header in overviews:
	subject, part_nr, total_parts, filename, segment_nr, total_segments = pattern.match(header['subject']).groups()
	segment = {'message-id':header['message-id'], 'bytes':header[':bytes']}
	if subject in subjects:
		if part_nr in subjects[subject]['parts']:
			subjects[subject]['parts'][part_nr]['segments'][segment_nr] = segment
		else:		
			part = {'name':filename, 'total_segments':total_segments, 'poster':header['from'], 'date':header['date'], 'segments':{segment_nr:segment}}
			subjects[subject]['parts'][part_nr] = part
	else:
		part = {'name':filename, 'total_segments':total_segments, 'poster':header['from'], 'date':header['date'], 'segments':{segment_nr:segment}}
		subjects[subject] = {'total_parts':total_parts, 'parts':{part_nr:part}}
t2 = time()
print('organized %s headers in %f seconds' % (n_headers,(t2-t1)))

for s in subjects:
	print('%s: %s of %s parts' % (s,len(subjects[s]['parts']),subjects[s]['total_parts']))
