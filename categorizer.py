import os
from iris_helper import IrisHelper
from regex_helper import ListHelper
from listings import garbagedomains, leodomains
from settings import config_by_name

settings = config_by_name[os.getenv('sysenv') or 'dev']

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
    close_keys = ['copyright', 'trademark', 'infringement']

    phish_cat = l.reg_logic(tickets, phish_keys)
    phish_move(phish_cat[0])

    mal_cat = l.reg_logic(phish_cat[1], malware_keys)
    mal_move(mal_cat[0])

    net_cat = l.reg_logic(mal_cat[1], netabuse_keys)
    net_move(net_cat[0])

    spam_cat = l.reg_logic(net_cat[1], spam_keys)
    spam_move(spam_cat[0])

    close_cat = l.reg_logic(spam_cat[1], close_keys)
    for ticket in close_cat[0]:
        i.ticket_close(ticket)

    leftovers(close_cat[1])

    return True


def phish_move(move_list):

    for ticket in move_list:
        i.ticket_move(ticket, settings.phish_service_id, '15550')


def mal_move(move_list):
    for ticket in move_list:
        i.ticket_move(ticket, settings.mal_service_id, '15550')


def net_move(move_list):
    for ticket in move_list:
        i.ticket_move(ticket, settings.net_service_id, '15550')


def spam_move(move_list):
    for ticket in move_list:
        i.ticket_move(ticket, settings.spam_service_id, '15550')


def leftovers(update_list):
    for ticket in update_list:
        i.ticket_update(ticket, '15550')

if __name__ == '__main__':
    print categorize()
