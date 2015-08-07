#! /usr/bin/python3
import nntplib, re, logging, sys
from config import auth
from datetime import datetime, timezone, timedelta
from dateutil.parser import parse
#from time import time

FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
logging.basicConfig(format=FORMAT,level=logging.DEBUG)
logger = logging.getLogger('ko-indexer')
TIME_FORMAT = "%a, %d %b %Y %H:%M:%S %z"

def init_connection(host=auth[0]['server'],user=auth[0]['username'],password=auth[0]['password']):
	return nntplib.NNTP(host=host, user=user, password=password)

def get_article_count(conn, group):
	_, count, first, last, _ = conn.group(group)
	logger.info('There are %d articles in %s, the first is %d, the last is %d' % (count, group, first, last))

def get_articles_by_age(conn, days, group):
	_, now = conn.date()
	now = now.replace(tzinfo=timezone(timedelta(0,0)))
	delta = timedelta(days=days)
	wishdate = now - delta
	accuracy = timedelta(hours=1)
	_,_,_,last,_ = conn.group(group)
	position = last//2
	width = position
	prev_current = now
	while delta > accuracy:
		current = parse(conn.over((position,position))[1][0][1]['date'])
		if prev_current == current:
			break
		delta = current - wishdate
		d = now - current
		logger.info('Positon: %d Age: %.2f days' % (position, d.days+d.seconds/86400))
		width = width//2
		if current > wishdate:
			position = position - width			
		else:
			position = position + width
		if delta < timedelta(0):
			delta = delta * -1
		prev_current = current

def main():
	conn = init_connection()
	group = sys.argv[1]
	days = int(sys.argv[2])
	get_article_count(conn, group)
	get_articles_by_age(conn,days,group)
	conn.quit()	

if __name__ == '__main__':
	main()
	
