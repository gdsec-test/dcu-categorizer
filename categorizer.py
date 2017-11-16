from iris_helper import IrisHelper
from regex_helper import ListHelper
from listings import garbagedomains, leodomains

i = IrisHelper()
l = ListHelper()


def cleanup():
    garbage = []
    cleaning = garbagedomains
    for a in cleaning:
        trash = i.ticket_finder(a)
        for t in trash:
            garbage.append(t[0])

    return garbage


def leomove():
    leo = []
    moving = leodomains
    for a in moving:
        sort = i.ticket_finder(a)
        for t in sort:
            leo.append(t[0])

    return leo


def categorize():

    tickets = i.data_pull()

    phish_keys = ['phishing', 'phish', 'fishing', 'fish']
    malware_keys = ['malware', 'virus']
    netabuse_keys = ['botnet', 'intrusion', 'scan', 'attempted login', 'login attempted', 'ssh', 'brute']
    spam_keys = ['spam', 'spoof', 'spoofed']
    transfer_keys = ['copyright', 'trademark', 'infringement']

    phish_cat = l.reg_logic(tickets, phish_keys)
    #m_list = phish_cat[1]
    #phish_cat = phish_cat[0]

    # print i.data_pull()

    # return phish_cat, m_list

    return phish_cat

if __name__ == '__main__':
    print categorize()
