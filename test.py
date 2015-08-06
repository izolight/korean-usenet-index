#! /usr/bin/python3
import nntplib, re, logging, sys
from config import auth
from time import time

FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
logging.basicConfig(format=FORMAT,level=logging.DEBUG)
logger = logging.getLogger('ko-indexer')

def init_connection(host=auth[0]['server'],user=auth[0]['username'],password=auth[0]['password']):
	return nntplib.NNTP(host=host, user=user, password=password)

def get_article_count(conn, group):
	_, count, first, last, _ = conn.group(group)
	logger.info('There are %d articles in %s, the first is %d, the last is %d' % (count, group, first, last))

def main():
	conn = init_connection()
	group = sys.argv[1]
	get_article_count(conn, group)
	conn.quit()	

if __name__ == '__main__':
	main()
	
