import os
from iris_helper import IrisHelper
from regex_helper import ListHelper
from listings import garbagedomains, leodomains
from settings import config_by_name

settings = config_by_name[os.getenv('sysenv') or 'dev']


class Categorizer:

    def __init__(self, logger):
        self.i = IrisHelper()
        self.l = ListHelper()
        self.eid = settings.phishstory_eid
        self._logger = logger

    def cleanup(self):
        incidents = self.i.ticket_finder(garbagedomains, settings.abuse_service_id, settings.ds_abuse_group_id)
        self._logger.info('Completed cleanup function...\n Cleanup tickets: {}'.format(incidents))
        for incident in incidents:
            self.i.ticket_close(incident)

    def leomove(self):
        incidents = self.i.ticket_finder(leodomains, settings.abuse_service_id, settings.dcu_group_id)
        self._logger.info('Completed leomove function...\n Leomove tickets: {}'.format(incidents))
        for incident in incidents:
            self.i.ticket_move(incident, settings.leo_service_id, settings.dcu_group_id, 0)

    def categorize(self):

        tickets = self.i.data_pull()

        phish_keys = ['phishing', 'phish', 'fishing', 'fish', 'scam', 'scammers', 'scammer', 'pishing', 'plishing', 'phising',
                      'fraudulent']
        malware_keys = ['malware', 'virus', 'trojan']
        netabuse_keys = ['botnet', 'intrusion', 'scan', 'attempted login', 'login attempted', 'ssh', 'brute', 'hacking',
                         'honeypot', 'abusix', 'rogue DNS', 'attack', 'attacks', 'crack', 'hack', 'logon', 'log-on',
                         'signon', 'sign-on']
        spam_keys = ['spam', 'spoof', 'spoofed', 'trans.', 'fw:', 'fwd:']
        close_keys = ['copyright', 'trademark', 'infringement', 'seo', 'lahjakortti', 'proposal', 'gorakshnath',
                      'pikavipit', 'lainaa', 'defamation', 'lainatarjoukseen', 'attendee', 'attendees', 'promotional',
                      'leads', 'donation', 'sell', 'sale', 'manufacturer', '1st page', 'training', 'loan', 'loans',
                      'black friday', 'purchase domain', 'buy domain', 'buying domain', 'purchase order', 'eyelash',
                      'convention', 'cctv', 'attendance', 'job offer', 'cyber monday', 'prize', 'event ideas', 'led',
                      'lighting', 'supplier', 'supplies', 'order status', 'pcb', 'seminar', 'revamp', 'revamping',
                      'web design', u'\u552E']

        buckets = {}

        phish_cat = self.l.reg_logic(tickets, phish_keys)
        self._logger.info('Phishing incidents moved: {}'.format(phish_cat[0]))
        self._move(settings.phish_service_id, phish_cat[0], settings.csa_group_id, self.eid)
        buckets['phishing'] = phish_cat[0]

        mal_cat = self.l.reg_logic(phish_cat[1], malware_keys)
        self._logger.info('Malware incidents moved: {}'.format(mal_cat[0]))
        self._move(settings.mal_service_id, mal_cat[0], settings.csa_group_id, self.eid)
        buckets['malware'] = mal_cat[0]

        net_cat = self.l.reg_logic(mal_cat[1], netabuse_keys)
        self._logger.info('Netabuse incidents moved: {}'.format(net_cat[0]))
        self._move(settings.net_service_id, net_cat[0], settings.csa_group_id, self.eid)
        buckets['netabuse'] = net_cat[0]

        spam_cat = self.l.reg_logic(net_cat[1], spam_keys)
        self._logger.info('Spam incidents moved: {}'.format(spam_cat[0]))
        self._move(settings.spam_service_id, spam_cat[0], settings.csa_group_id, self.eid)
        buckets['spam'] = spam_cat[0]

        close_cat = self.l.reg_logic(spam_cat[1], close_keys)
        self._logger.info('Tickets being closed: {}'.format(close_cat[0]))
        for ticket in close_cat[0]:
            self.i.ticket_close(ticket)
        buckets['close'] = close_cat[0]

        leftovers = []
        for ticket in close_cat[1]:
            leftovers.append(ticket)

        self.leftovers(close_cat[1], self.eid)
        self._logger.info('Leftover tickets: {}'.format(leftovers))
        buckets['left'] = close_cat[1]

        self.i.the_closer()

        return buckets

    def _move(self, service_id, move_list, groupid, eid):

        for ticket in move_list:
            result = self.i.ticket_move(ticket, service_id, groupid, eid)
            if result:
                self._logger.info('Succesfully moved: {}'.format(ticket))

    def leftovers(self, update_list, eid):
        for ticket in update_list:
            self.i.ticket_update(ticket, eid)
