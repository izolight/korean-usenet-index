#!/usr/bin/python3

import unittest
import nntplib
import re

config = {
    'server': '***REMOVED***',
    'user': '***REMOVED***',
    'password': '***REMOVED***',
}

class Usenet:
    
    def __init__(self):
        self.conn = self.connect()

    def connect(self):
        conn = nntplib.NNTP_SSL(host=config['server'], user=config['user'], password=config['password'])
        return conn
    
    def quit(self):
        self.conn.quit()

    def set_group(self, group):
        r, c, f, l, n = self.conn.group(group)
        self.count = c
        self.first = f
        self.last = l
        self.group = n

    def get_latest_headers(self, num_headers):
        r, ovs = self.conn.over((self.last-num_headers, self.last))
        binaries = {}
        part_regex = re.compile(r"^(?P<subject>.+?) \((?P<num>\d+)\/(?P<num_parts>\d+)\)$")
        for num, ov in ovs:
            try:
                subject,num,num_parts = part_regex.match(ov['subject']).groups()
            except AttributeError:
                print("not matched: %s" % ov['subject'])
                continue
            if subject not in binaries:
                binaries[subject] = 0
                print(subject)
            binaries[subject] += 1

class TestUsenetMethods(unittest.TestCase):
    
    def test_set_group(self):
        group = 'korea.binaries.tv'
        u = Usenet()
        u.set_group(group)
        self.assertEqual(u.group, group)
        u.quit()      
    
    def test_first_last(self):
        group = 'korea.binaries.tv'
        u = Usenet()
        u.set_group(group)
        self.assertGreater(u.last, 60000000)
        self.assertLess(u.first, 10)
        u.quit()
    
    def test_headers(self):
        group = 'korea.binaries.tv'
        u = Usenet()
        u.set_group(group)
        u.get_latest_headers(500)
        self.assertEqual(1,1)
        u.quit()

if __name__ == '__main__':
    unittest.main()
