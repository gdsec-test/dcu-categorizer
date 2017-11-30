import pyodbc
import os
import suds.client
import suds.sax.text
from settings import config_by_name
import xmltodict

settings = config_by_name[os.getenv('sysenv') or 'dev']


class IrisHelper:

    def __init__(self, logger):
        self.dbstring = settings.dbstring
        self._logger = logger
        # connection to DB server
        try:
            self.cnxn = pyodbc.connect(self.dbstring)
        except Exception as e:
            self._logger.error('Connection to IRIS DB failed: {}'.format(e))

        self._client = suds.client.Client(settings.wsdl_url)
        self.closed_note = "This ticket has been closed by DCU-ENG automation as unworkable. Questions to hostsec@"

    def data_pull(self):
        """
        pulls IID and summary line from all open tickets in IRIS Abuse@ queue
        :return:
        """
        group_id = settings.ds_abuse_group_id
        service_id = settings.abuse_service_id

        query = 'SELECT TOP 200 iris_incidentID, OriginalEmailAddress FROM [iris].[dbo].[IRISIncidentMain] ' \
                'WITH(NOLOCK) ' \
                'WHERE iris_groupID = ' + group_id + ' AND iris_serviceID = ' + service_id + ' ' \
                'AND iris_employeeID = 0 and iris_statusID = 1 ' \
                'ORDER BY createDate'

        return self._iris_db_connect(query)

    def ticket_close(self, incident):
        """
        closes tickets with note stating unworkable ticket
        phishtory
        :param incident:
        :return:
        """
        phishstory_employee_id = 15550
        try:
            self._client.service.AddIncidentNote(
                int(incident),
                self.closed_note.format(), settings.notation_user)
            self._client.service.QuickCloseIncident(
                int(incident),
                phishstory_employee_id, )
        except Exception as e:
            self._logger.error("Auto Close failed on IID: {}, {}".format(incident, e))

    def note_puller(self, iid):
        """
        Retrieves notes from ticket using SOAP call to IRIS Webservice
        :param iid: IRIS Incident ID
        :return:
        """

        self._logger.info('Gathering info for: %s', iid)

        xml_string = suds.sax.text.Raw("<ns0:IncidentId>" + str(iid) +
                                       "</ns0:IncidentId>")

        try:
            incident_info = dict(self._client.service.GetIncidentInfoByIncidentId(xml_string))

        except Exception as e:
            self._logger.error('Unable to retrieve incident info: {}'.format(e.message))

        email = incident_info['ToEmailAddress']
        subject = incident_info['Subject']

        notes_text = self._client.service.GetIncidentCustomerNotes(iid, 0)
        note_dict = xmltodict.parse(notes_text)

        note = note_dict['NotesByIncident']['Notes']['Item']['@Note']

        return email, subject, note

    def ticket_update(self, iid, serviceid, groupid, eid):
        """
        This function is designed to take in an IRIS Incident ID and a Service ID to move the IID too using an IRIS DB
        stored procedure
        :param iid:
        :param serviceid:
        :param eid:
        :param groupid:
        :return:
        """

        query = """\
        SET CONCAT_NULL_YIELDS_NULL, ANSI_WARNINGS, ANSI_PADDING ON;
        SET IMPLICIT_TRANSACTIONS OFF;
        DECLARE @b_checkdatepass bit;
        EXEC IRIS_IncidentMainUpdate_sp @n_incidentID = ?, @n_ServiceID = ?, @n_iris_groupID = ?, @vc_modifiedBy = 'DCU Abuse cleanup', @n_iris_employeeID = ?, @b_checkdatepass = @b_checkdatepass output;
        SELECT @b_checkdatepass AS the_output;"""

        params = (iid, serviceid, groupid, eid)

        self._iris_db_connect(query, params)

    def _iris_db_connect(self, query, params=None):
        """
        Used to fire IRIS DB queries, checks for params
        :param query:
        :param params:
        :return:
        """

        self.cnxn.autocommit = True
        self.cnxn.timeout = 0
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
