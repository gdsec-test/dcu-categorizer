import json
import logging

import listings
from email_classifier import EmailClassifier
from iris_helper import IrisHelper
from regex_helper import ListHelper


class Categorizer:

    def __init__(self, app_settings):
        self._logger = logging.getLogger(__name__)

        self._iris_helper = IrisHelper(app_settings)
        self._list_helper = ListHelper()

        self.eid = app_settings.phishstory_eid

        # Group IDs
        self.abuse_group = app_settings.ds_abuse_group_id
        self.csa_group_id = app_settings.csa_group_id
        self.dcu_group = app_settings.dcu_group_id

        # Service IDs
        self.leo_id = app_settings.leo_service_id
        self.abuse_id = app_settings.abuse_service_id
        self.childabuse_service_id = app_settings.childabuse_service_id
        self.phish_service_id = app_settings.phish_service_id
        self.mal_service_id = app_settings.mal_service_id
        self.net_service_id = app_settings.net_service_id

        # Email IDs
        self.abuse_email_id = app_settings.abuse_email_id
        self.leo_email_id = app_settings.leo_email_id
        self.classifier = EmailClassifier(app_settings.categorizer_username, app_settings.categorizer_password,
                                          app_settings.email_api_url, app_settings.jwt_url, app_settings.cert_path,
                                          app_settings.key_path)

        # This value allows us to sort 95% of the emails that the classifier predicts on
        self.THRESHOLD = 0.9108867987360374

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
                self._iris_helper.close_ticket(iid)
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
                self._iris_helper.update_ticket(iid, self.leo_id, self.dcu_group, 0, self.leo_email_id)
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
        incident_dict = {}
        for iid in incidents.iterkeys():
            text = self._iris_helper.get_notes(iid)
            subject = text[1] or ''
            body = text[2] or ''

            incident_dict[iid] = (subject, body)

        try:
            for incident, (subject, body) in incident_dict.items():
                response = self.classifier.get_prediction((subject, body))
                response = json.loads(response.content)
                prediction = response['prediction']
                if response['confidences'][prediction] < self.THRESHOLD:
                    self.leftovers(self.abuse_id, incident, self.abuse_group, self.eid)
                    self._logger.info('Leftover tickets: {}'.format(incident))
                elif prediction == 'NETABUSE_EMAIL':
                    self._logger.info('Netabuse incidents moved: {}'.format(incident))
                    self._move(self.net_service_id, incident, self.csa_group_id, self.eid, self.abuse_email_id)
                elif prediction == 'MALWARE_EMAIL':
                    self._logger.info('Malware incidents moved: {}'.format(incident))
                    self._move(self.mal_service_id, incident, self.csa_group_id, self.eid, self.abuse_email_id)
                elif prediction == 'PHISHING_EMAIL':
                    self._logger.info('Phishing incidents moved: {}'.format(incident))
                    self._move(self.phish_service_id, incident, self.csa_group_id, self.eid, self.abuse_email_id)
                elif prediction == 'CSAM_EMAIL':
                    self._logger.info('CSAM incidents moved: {}'.format(incident))
                    self._move(self.childabuse_service_id, incident, self.dcu_group, self.eid, self.abuse_email_id)

        except Exception as e:
            self._logger.error('Unable to complete Categorizer: {}'.format(e.message))

        finally:
            self._iris_helper.the_closer()

    def _move(self, service_id, ticket_iid, groupid, eid, emailid):
        """
        Takes list of tickets to move and calls IRIS DB Stored Procedure to update ticket to new queue
        :param service_id: in settings
        :param move_list: in settings
        :param groupid: in settings
        :param eid: in settings
        :param emailid: in settings
        :return:
        """
        result = self._iris_helper.update_ticket(ticket_iid, service_id, groupid, eid, emailid)
        if result:
            self._logger.info('Succesfully moved: {}'.format(ticket_iid))

    def leftovers(self, service_id, update_ticket, groupid, eid):
        """
        Takes list of tickets that are left after all other functions have run, assigns ticket to Phishtory, CSA
        :param service_id:
        :param update_list:
        :param groupid:
        :param eid:
        :return:
        """
        self._logger.info('Assigning ticket to Phishtory, CSA: {}'.format(update_ticket))
        self._iris_helper.update_ticket(update_ticket, service_id, groupid, eid, self.abuse_email_id)

    def _email_helper(self, email):
        """
        Used to avoid issues with Non email entires in the Email area of IRIS tickets
        :param email:
        :return:
        """
        if '@' in email:
            email = email.split('@')[1]

        return email
