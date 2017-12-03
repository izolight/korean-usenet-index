#! /usr/bin/python3
import nntplib
from dateutil.parser import parse
from config import auth

class Indexer():
    def __init__(self):
        self.connection = nntplib.NNTP_SSL(host=auth['server'],user=auth['user'],password=auth['password'])

    # For Setting the group and updating first/last
    def set_Group(self, groupname):
        conn = self.connection
        self.resp, cnt, first, last, group = conn.group(groupname)
        self.count = cnt
        self.first = first
        self.last = last
        self.group = group            
        self.firstdate = parse(conn.over((first,first))[1][0][1]['date'])
        self.lastdate = parse(conn.over((last,last))[1][0][1]['date'])

    def get_latest_headers(self, num_headers):
        conn = self.connection
        try:
            self.set_Group(self.group)
            resp, overviews = conn.over((self.last-num_headers,self.last))
            self.last_headers = overviews
        except AttributeError:
            print('set group first')
