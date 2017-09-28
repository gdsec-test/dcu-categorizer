from iris_helper import Iris_helper
from settings import dbstring

i = Iris_helper(dbstring)

def cleanup():
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
    print i.data_pull()
    phish_cat = []
    malware_cat =[]
    netabuse_cat = []
    spam_cat = []
    garbage_cat = []

    phish_keys = ['phishing', 'phish']
    malware_keys = ['malware', 'virus']
    netabuse_keys = ['botnet', 'intrusion', 'scan', 'attempted login', 'login attempted']
    spam_keys = ['spam', 'spoof', 'spoofed']
    garbage_keys = ['copyright', 'trademark', 'infringement']

    #ToDo setup regex seperated by category for use in this function


    pass

if __name__ == '__main__':
    categorize()
