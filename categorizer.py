import os
from iris_helper import IrisHelper
from regex_helper import ListHelper
from listings import garbagedomains, leodomains
from settings import config_by_name

settings = config_by_name[os.getenv('sysenv') or 'dev']


class Categorizer:

    def __init__(self):
        self.i = IrisHelper()
        self.l = ListHelper()

    def cleanup(self):
        garbage = []
        cleaning = garbagedomains
        for a in cleaning:
            trash = self.i.ticket_finder(a)
            for t in trash:
                garbage.append(t[0])

        return garbage

    def leomove(self):
        leo = []
        moving = leodomains
        for a in moving:
            sort = self.i.ticket_finder(a)
            for t in sort:
                leo.append(t[0])

        return leo

    def categorize(self):

        tickets = self.i.data_pull()

        phish_keys = ['phishing', 'phish', 'fishing', 'fish']
        malware_keys = ['malware', 'virus']
        netabuse_keys = ['botnet', 'intrusion', 'scan', 'attempted login', 'login attempted', 'ssh', 'brute']
        spam_keys = ['spam', 'spoof', 'spoofed']
        close_keys = ['copyright', 'trademark', 'infringement']

        phish_cat = l.reg_logic(tickets, phish_keys)
        self.phish_move(phish_cat[0])

        mal_cat = l.reg_logic(phish_cat[1], malware_keys)
        self.mal_move(mal_cat[0])

        net_cat = l.reg_logic(mal_cat[1], netabuse_keys)
        self.net_move(net_cat[0])

        spam_cat = l.reg_logic(net_cat[1], spam_keys)
        self.spam_move(spam_cat[0])

        close_cat = l.reg_logic(spam_cat[1], close_keys)
        for ticket in close_cat[0]:
            self.i.ticket_close(ticket)

        self.leftovers(close_cat[1])

        self.i.the_closer()

        return True

    def phish_move(self, move_list):

        for ticket in move_list:
            self.i.ticket_move(ticket, settings.phish_service_id, '15550')

    def mal_move(self, move_list):
        for ticket in move_list:
            self.i.ticket_move(ticket, settings.mal_service_id, '15550')

    def net_move(self, move_list):
        for ticket in move_list:
            self.i.ticket_move(ticket, settings.net_service_id, '15550')

    def spam_move(self, move_list):
        for ticket in move_list:
            self.i.ticket_move(ticket, settings.spam_service_id, '15550')

    def leftovers(self, update_list):
        for ticket in update_list:
            self.i.ticket_update(ticket, '15550')
