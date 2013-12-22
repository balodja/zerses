#!/usr/bin/python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import sys
import os
import re
import datetime
import unicodedata

#sys.argv.append('./2010/08/25.html')

# Check args
if len(sys.argv) != 2:
    sys.stderr.write("Error: file name as the only argument is needed\n")
    exit(1)

filename = sys.argv[1]
if not (os.path.exists(filename) and os.path.isfile(filename)):
    sys.stderr.write("Error: that's not the file name\n")
    exit(2)


def getdate_from_filename(filename):
    fullpath = os.path.abspath(filename)
    (other, day) = os.path.split(fullpath)
    day = day.rstrip('.html')
    (other, month) = os.path.split(other)
    (other, year) = os.path.split(other)
    return datetime.date(int(year), int(month), int(day))

def getmsg_under_tag(tag):
    msg = []
    msgtag = tag
    while msgtag != '\n' and hasattr(msgtag.next, 'name') and msgtag.next.name == 'br':
        msg.append(msgtag)
        msgtag = msgtag.next.next
    if len(msg) % 4 == 0:
        return '\n'.join(intersperse(msg))
    return '\n'.join(msg)

def intersperse(lst):
    if len(lst) <= 4:
        return lst
    else:
        return lst[:4] + [''] + intersperse(lst[4:])

def translate_entref(s):
    return s.replace('&nbsp;', ' ').replace('&amp;', '\\&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '\"').replace('&apos;', '`').replace('_', '\\_')

def is_zerse(msg):
#    cyrs = 0
    cyrcaps = 0
    newlines = 0
    for c in msg:
        charname = unicodedata.name(c, 'unknown')
        if charname.startswith('CYRILLIC CAPITAL'):
            cyrcaps += 1
        elif c == '\n':
            newlines += 1
#            cyrs += 1
#        elif charname.startswith('CYRILLIC'):
#            cyrs += 1
	if msg.find('\\\\') != -1:
		return False
    if newlines >= 1 and float(cyrcaps)/len(msg) > 0.2:
        return True
    return False

def format_zerse(msg, nick, dt):
    return \
           '\\begin{minipage}{\\textwidth}' + \
           '\\poemtitle{***}\n' + \
           '\\begin{verse}\n' + \
           msg.strip().replace('\n', '\\\\\n').replace('\\\\\n\\\\','\\\\!') + '\n' + \
           '\\attrib{%s, %s}\n' % (nick, dt) + \
           '\\end{verse}\n' + \
           '\\end{minipage}\n'

# Now, let's do it
soup = BeautifulSoup(open(filename))
date = getdate_from_filename(filename)

for tag in soup.findAll('font', {'class':'mn'}):
    timestamp = tag.findPrevious('a').next
    time = datetime.datetime.strptime(timestamp, '[%H:%M:%S]').time()
    nick = tag.next[4:-4]
    #print timestamp
    msg = getmsg_under_tag(tag.next.next)
    if is_zerse(msg):
        dt = datetime.datetime.combine(date, time).strftime('%a %b %d %H:%M:%S %Y')
        print translate_entref(format_zerse(msg, nick, dt)).encode('utf8')
