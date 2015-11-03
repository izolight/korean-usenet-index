#!/usr/bin/python3
import nntplib, sys, re
from config import auth

s0 = nntplib.NNTP_SSL(host=auth[0]['server'],user=auth[0]['username'],password=auth[0]['password'])
s1 = nntplib.NNTP_SSL(host=auth[1]['server'],user=auth[1]['username'],password=auth[1]['password'])
s2 = nntplib.NNTP_SSL(host=auth[2]['server'],user=auth[2]['username'],password=auth[2]['password'])

msgid_regex = '^<[^@]+@[^@]+>$'

def main():
    group = sys.argv[1]
    try:
        print('Highwinds')
        _, _, _, last, _ = s0.group(group)
        print(s0.xhdr('subject',last))
    except nntplib.NNTPTemporaryError:
        pass    

    try:    
        print('XSNews')
        _, _, _, last, _ = s1.group(group)
        print(s1.xhdr('subject',last))
    except nntplib.NNTPTemporaryError:
        pass

    try:
        print('Newsoo')
        _, _, _, last, _ = s2.group(group)
        print(s2.xhdr('subject',last))
    except nntplib.NNTPTemporaryError:
        pass


if __name__ == '__main__':
    main()
