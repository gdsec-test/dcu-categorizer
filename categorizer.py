from iris_helper import Iris_helper
from settings import dbstring

i = Iris_helper(dbstring)

def cleanup():
    #ToDo run trash_man and call ticket close
    address = ['sh.baidu.com', 'notices.nr-online.com', 'legal-notification.com', 'woody.ch', 'justdeals.com',
                   'certifiedmart.com', 'marcon-media.de', 'newsletter.kopp-verlag.de', 'brandshop.com', 'law360.com',
                   'ogrupo.org.br', 'domainerschoice.com', '163.com', 'peakindustry.com', 'woody.ch', 'foxmail.com',
                   'sina.cn', 'sina.com', 'appleitunesguide.com', 'notice.bizcn.com']
    garbage = []
    for a in address:
        trash = i.trash_man(a)
        for t in trash:
            garbage.append(t[0])

    print garbage

def categorize():
    #ToDo logic to check summary for keywords and create lists of IIDs to "move" Check out import re

    #ToDo setup regex seperated by category for use in this function
    """
    Keywords (in priority):
	Phishing (P)
	Phish (P)
	SPAM (S)
	Malware (M)
	Virus (M)
	Botnet (NA)
	Scan (NA)
	Scam (P)
	Intrusion (NA)
	attempted login (NA)
	login attempted (NA)
	Spoof (S)
	Fake (P)
	Copy (P)
	Copyright (Close)
	Trademark (Close)
	Infringement (Close)
    """
    pass

#ToDo setup script to run