import logging

import pyodbc
import suds.client
import suds.sax.text
import xmltodict


class IrisHelper:

    closed_note = 'This ticket has been closed by DCU-ENG automation as unworkable. Questions to hostsec@'

    def __init__(self, app_settings):
        self._logger = logging.getLogger(__name__)

        self._group_id = app_settings.ds_abuse_group_id
        self._service_id = app_settings.abuse_service_id
        self._phishstory_eid = app_settings.phishstory_eid
        self._notation_user = app_settings.notation_user

        try:
            self.cnxn = pyodbc.connect(app_settings.dbstring, autocommit=True)
        except Exception as e:
            self._logger.error('Connection to IRIS DB failed: {}'.format(e))

        try:
            self._client = suds.client.Client(app_settings.IRIS_WSDL)
        except Exception as e:
            self._logger.error('Connection to IRIS WSDL failed: {}'.format(e))

    def data_pull(self):
        """
        Pulls IID and summary line from all open tickets in IRIS Abuse@ queue
        :return:
        """

        query = 'SELECT TOP 200 iris_incidentID, OriginalEmailAddress FROM [iris].[dbo].[IRISIncidentMain] ' \
                'WITH(NOLOCK) ' \
                'WHERE iris_groupID = ' + self._group_id + ' AND iris_serviceID = ' + self._service_id + ' ' \
                'AND iris_employeeID = 0 and iris_statusID = 1 ' \
                'ORDER BY createDate'

        return self._iris_db_connect(query)

    def close_ticket(self, incident):
        """
        Closes tickets with note stating unworkable ticket
        phishtory
        :param incident:
        :return:
        """

        try:
            self._client.service.AddIncidentNote(
                int(incident),
                self.closed_note, self._notation_user)
            self._client.service.QuickCloseIncident(
                int(incident),
                self._phishstory_eid, )
        except Exception as e:
            self._logger.error('Auto Close failed on IID: {}: {}'.format(incident, e))

    def get_notes(self, iid):
        """
        Retrieves notes from ticket using SOAP call to IRIS Webservice
        :param iid: IRIS Incident ID
        :return:
        """

        self._logger.info('Gathering info for: {}'.format(iid))

        xml_string = suds.sax.text.Raw('<ns0:IncidentId>' + str(iid) + '</ns0:IncidentId>')

        try:
            incident_info = dict(self._client.service.GetIncidentInfoByIncidentId(xml_string))

        except Exception as e:
            self._logger.error('Unable to retrieve incident info: {}'.format(e.message))

        email = incident_info['ToEmailAddress'] or ''
        subject = incident_info['Subject'] or ''

        notes_text = self._client.service.GetIncidentCustomerNotes(iid, 0)
        note_dict = xmltodict.parse(notes_text)

        note = ''

        notes_check = note_dict.get('NotesByIncident').get('Notes')

        if notes_check:
            item_check = notes_check.get('Item')
            if isinstance(item_check, list):
                item_check = item_check[0]

            note = item_check.get('@Note', '')

        return email, subject, note

    def update_ticket(self, iid, serviceid, groupid, eid, emailid):
        """
        This function is designed to take in an IRIS Incident ID and a Service ID to move the IID too using an IRIS DB
        stored procedure
        :param iid: supplied
        :param serviceid: in settings
        :param eid: in settings
        :param groupid: in settings
        :param emailid: in settings
        :return:
        """

        query = """\
        SET CONCAT_NULL_YIELDS_NULL, ANSI_WARNINGS, ANSI_PADDING ON;
        SET IMPLICIT_TRANSACTIONS OFF;
        DECLARE @b_checkdatepass bit;
        EXEC IRIS_IncidentMainUpdate_sp @n_incidentID = ?, @n_ServiceID = ?, @n_iris_groupID = ?, @vc_modifiedBy = 'DCU Abuse cleanup', @n_iris_employeeID = ?, @n_inboxEmailID = ?, @b_checkdatepass = @b_checkdatepass output;
        SELECT @b_checkdatepass AS the_output;"""

        params = (iid, serviceid, groupid, eid, emailid)
        self._iris_db_connect(query, params)

    def _iris_db_connect(self, query, params=None):
        """
        Used to fire IRIS DB queries, checks for params
        :param query:
        :param params:
        :return:
        """

        cursor = self.cnxn.cursor()
        query = query.strip()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        data = cursor.fetchall()
        cursor.commit()
        cursor.close()

        return data

    def the_closer(self):
        """
        closes IRIS DB connection, called at end of run, avoids issue of opening/closing connection for each function
        :return:
        """

        self.cnxn.close()
