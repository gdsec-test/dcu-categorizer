import os
from iris_helper import IrisHelper
from regex_helper import ListHelper
from listings import garbagedomains, leodomains
from settings import config_by_name
import logging

settings = config_by_name[os.getenv('sysenv') or 'dev']


class Categorizer:

    def __init__(self):
        self.i = IrisHelper()
        self.l = ListHelper()
        self.eid = settings.phishstory_eid
        self._logger = logging.getLogger(__name__)

    def cleanup(self):
        incidents = self.i.ticket_finder(garbagedomains, settings.abuse_service_id)
        for incident in incidents:
            self.i.ticket_close(incident)

    def leomove(self):
        incidents = self.i.ticket_finder(leodomains)
        for incident in incidents:
            self.i.ticket_move(incident, settings.leo_service_id, 0)

    def categorize(self):

        tickets = self.i.data_pull()

        phish_keys = ['phishing', 'phish', 'fishing', 'fish']
        malware_keys = ['malware', 'virus']
        netabuse_keys = ['botnet', 'intrusion', 'scan', 'attempted login', 'login attempted', 'ssh', 'brute']
        spam_keys = ['spam', 'spoof', 'spoofed']
        close_keys = ['copyright', 'trademark', 'infringement']

        buckets = {}

        phish_cat = self.l.reg_logic(tickets, phish_keys)
        self._move(settings.phish_service_id, phish_cat[0], self.eid)
        buckets['phishing'] = phish_cat[0]

        mal_cat = self.l.reg_logic(phish_cat[1], malware_keys)
        self._move(settings.mal_service_id, mal_cat[0], self.eid)
        buckets['malware'] = mal_cat[0]

        net_cat = self.l.reg_logic(mal_cat[1], netabuse_keys)
        self._move(settings.net_service_id, net_cat[0], self.eid)
        buckets['netabuse'] = net_cat[0]

        spam_cat = self.l.reg_logic(net_cat[1], spam_keys)
        self._move(settings.spam_service_id, spam_cat[0], self.eid)
        buckets['spam'] = spam_cat[0]

        close_cat = self.l.reg_logic(spam_cat[1], close_keys)
        for ticket in close_cat[0]:
            self.i.ticket_close(ticket)
        buckets['close'] = close_cat[0]

        self.leftovers(close_cat[1], self.eid)
        buckets['left'] = close_cat[1]

        self.i.the_closer()

        return buckets

    def _move(self, service_id, move_list, eid):

        for ticket in move_list:
            result = self.i.ticket_move(ticket, service_id, eid)
            if result is True:
                self._logger.info('Succesfully moved: {}'.format(ticket))

    def leftovers(self, update_list, eid):
        for ticket in update_list:
            self.i.ticket_update(ticket, eid)
