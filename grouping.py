#! /usr/bin/python3
import nntplib, re
from config import auth
from time import time

fencoding = 'utf-8'
tencoding = 'cp1252'
errors = 'ignore'

s0 = nntplib.NNTP(host=auth[0]['server'],user=auth[0]['username'],password=auth[0]['password'])
pattern = re.compile(r"(?P<subject>.+?) \[(?P<part>\d{1,4})\/(?P<total_parts>\d{1,4})\] \- \"(?P<filename>.+?)\" yEnc \((?P<segment>\d{1,4})\/(?P<total_segments>\d{1,4})")
pattern2 = re.compile(r"(?P<subject>.+?)  \"(?P<filename>.+?)\" \[(?P<part>\d{1,4})\/(?P<total_parts>\d{1,4})\] \((?P<segment>\d{1,4})\/(?P<total_segments>\d{1,4})")

n_headers = 5000
resp, count ,first, last, name = s0.group('korea.binaries.tv')
t0 = time()
resp, overviews = s0.over((last-n_headers,last))
t1 = time()
print('got %s headers in %f seconds' % (n_headers,(t1-t0)))
subjects = {}

for number, header in overviews:
	match = pattern.match(header['subject'])
	if not match:
		match = pattern2.match(header['subject'])
		if not match:
			print(header['subject'])
			continue
	subject = match.group('subject')
	part_nr = int(match.group('part'))
	total_parts = int(match.group('total_parts'))
	filename = match.group('filename')
	segment_nr = int(match.group('segment'))
	total_segments = int(match.group('total_segments'))
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
	current_parts = len(subjects[s]['parts'])
	total_parts = subjects[s]['total_parts']
	subjects[s]['complete'] = False
	if current_parts == total_parts:
		subjects[s]['complete'] = True
		for part in subjects[s]['parts']:
			current_segments = len(subjects[s]['parts'][part]['segments'])
			total_segments = subjects[s]['parts'][part]['total_segments']
			if current_segments != total_segments:
				subjects[s]['complete'] = False
	print('%s %s' % (s,subjects[s]['complete']))
#	if subjects[s]['complete']:
#		print(s)
