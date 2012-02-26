#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Leon Hui
# email:  cassvin91@gmail.com

import urllib
import sys
from pyquery.pyquery import PyQuery

#reload(sys)
#sys.setdefaultencoding('UTF-8')

URL = 'http://dict.hjenglish.com/app/w/'

class NoneError(Exception):
    pass

def tr(itext):
    if not itext:
        raise NoneError
    global URL 
    url = URL + urllib.quote(itext)
    resp = urllib.urlopen(url)
    html = resp.read()
    resp.close()
    return extract_otext(html)

def extract_otext(html):
    pqhtml = PyQuery(html)
    pron = pqhtml('.trsf')
    mean = pqhtml('#panel_comment')
    rs = {}

    # 提取单词发音部分
    if pron:
        if pron.size() == 1:
            s = '%s' % pron.eq(0).text()
        else:
            s = '%s: %s; ' % (pron.eq(0).attr('title'), pron.eq(0).text())
            s += '%s: %s ' % (pron.eq(1).attr('title'), pron.eq(1).text())
        rs['pron'] = s

    # 提取单词意义部分
    if mean:
        s = mean.html().replace('<br />', '').replace('&#13', '')
        rs['mean'] = s

    return rs

if __name__ == '__main__':

    print 'Welcome to Leon Hui\'s translator gadget!'
    
    while True:
        try:
            itext = raw_input('>>> ').strip()
            itext = itext.split()[0] if itext else None
            rs = tr(itext)
        except NoneError:
            continue
        except EOFError:
            print '\r'
            sys.exit(0)
        except KeyboardInterrupt:
            print '\r'
            continue
        except IOError, e:
            print 'Error: %s' % e
            continue
        else:
            print rs['pron'] if rs.get('pron') else None
            print rs['mean'] if rs.get('mean') else None
        
