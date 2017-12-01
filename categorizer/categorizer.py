import os
from iris_helper import IrisHelper
from regex_helper import ListHelper
import listings
from settings import config_by_name

settings = config_by_name[os.getenv('sysenv') or 'dev']


class Categorizer:

    def __init__(self, logger):
        self.l = ListHelper()
        self.eid = settings.phishstory_eid
        self._logger = logger
        self.i = IrisHelper(self._logger)
        self.abuse_id = settings.abuse_service_id
        self.abuse_group = settings.ds_abuse_group_id
        self.leo_id = settings.leo_service_id
        self.dcu_group = settings.dcu_group_id
        self.phishstory_eid = '15550'

    def cleanup(self, incidents):
        """
        Looks at provided dictionary of tickets, pulls domain off of email, checks if in set of domains, closes matches
        :param incidents: dictionary with IIDs for Key, email for value
        :return:
        """
        domains = listings.garbagedomains
        remove = []

        for iid, email in incidents.iteritems():
            email = self._email_helper(email)
            if email in domains:
                self.i.ticket_close(iid)
                remove.append(iid)

        for iid in remove:
            incidents.pop(iid)

        self._logger.info('Completed cleanup function...\n Cleanup tickets: {}'.format(remove))

        return incidents

    def leomove(self, incidents):
        """
        Looks at provided dictionary of tickets, pulls domain off of email, checks if in set of domains, closes matches
        :param incidents: dictionary with IIDs for Key, email for value
        :return:
        """

        domains = listings.leodomains
        remove = []

        for iid, email in incidents.iteritems():
             email = self._email_helper(email)
             if email in domains:
                self.i.ticket_update(iid, self.leo_id, self.dcu_group, 0)
                remove.append(iid)

        for iid in remove:
            incidents.pop(iid)

        self._logger.info('Completed leomove function...\n Leomove tickets: {}'.format(remove))

        return incidents

    def categorize(self, incidents):
        """
        Takes dictionary if tickets, pulls subject and body of each ticket with SOAP call to IRIS Webservice
        Passes subject, body to regex and sorts IIDs to buckets and moves to appropriate queues
        :param incidents: dictionary with IIDs for Key, email for value
        :return:
        """

        buckets = {}
        incident_dict = {}

        for iid in incidents.iterkeys():
            text = self.i.note_puller(iid)
            subject = text[1] or ''
            body = text[2] or ''

            incident_dict[iid] = (subject, body)

        try:

            phish_cat = self.l.reg_logic(incident_dict, listings.phish_keys)
            self._logger.info('Phishing incidents moved: {}'.format(phish_cat[0]))
            self._move(settings.phish_service_id, phish_cat[0], settings.csa_group_id, self.eid)
            buckets['phishing'] = phish_cat[0]

            mal_cat = self.l.reg_logic(phish_cat[1], listings.malware_keys)
            self._logger.info('Malware incidents moved: {}'.format(mal_cat[0]))
            self._move(settings.mal_service_id, mal_cat[0], settings.csa_group_id, self.eid)
            buckets['malware'] = mal_cat[0]

            net_cat = self.l.reg_logic(mal_cat[1], listings.netabuse_keys)
            self._logger.info('Netabuse incidents moved: {}'.format(net_cat[0]))
            self._move(settings.net_service_id, net_cat[0], settings.csa_group_id, self.eid)
            buckets['netabuse'] = net_cat[0]

            spam_cat = self.l.reg_logic(net_cat[1], listings.spam_keys)
            self._logger.info('Spam incidents moved: {}'.format(spam_cat[0]))
            self._move(settings.spam_service_id, spam_cat[0], settings.csa_group_id, self.eid)
            buckets['spam'] = spam_cat[0]

            close_cat = self.l.reg_logic(spam_cat[1], listings.close_keys)
            self._logger.info('Tickets being closed: {}'.format(close_cat[0]))
            for ticket in close_cat[0]:
                self.i.ticket_close(ticket)
            buckets['close'] = close_cat[0]

            self.leftovers(self.abuse_id, close_cat[1], self.abuse_group, self.eid)
            leftover_iids = []
            for iid in close_cat[1].iterkeys():
                leftover_iids.append(iid)
            self._logger.info('Leftover tickets: {}'.format(leftover_iids))

        except Exception as e:
            self._logger.error('Unable to complete Categorizer: {}'.format(e.message))

        finally:
            self.i.the_closer()

    def _move(self, service_id, move_list, groupid, eid):
        """
        Takes list of tickets to move and calls IRIS DB Stored Procedure to update ticket to new queue
        :param service_id:
        :param move_list:
        :param groupid:
        :param eid:
        :return:
        """

        for ticket in move_list:
            result = self.i.ticket_update(ticket, service_id, groupid, eid)
            if result:
                self._logger.info('Succesfully moved: {}'.format(ticket))

    def leftovers(self, service_id, update_list, groupid, eid):
        """
        Takes list of tickets that are left after all other functions have run, assigns ticket to Phishtory, CSA
        :param service_id:
        :param update_list:
        :param groupid:
        :param eid:
        :return:
        """
        for ticket in update_list:
            self._logger.info('Assigning ticket to Phishtory, CSA: {}'.format(ticket))
            self.i.ticket_update(ticket, service_id, groupid, eid)

    def _email_helper(self, email):
        """
        Used to avoid issues with Non email entires in the Email area of IRIS tickets
        :param email:
        :return:
        """
        if '@' in email:
            email = email.split('@')[1]

        return email
