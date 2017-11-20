import pyodbc
import os
import suds
import logging
from settings import config_by_name

settings = config_by_name[os.getenv('sysenv') or 'dev']


class IrisHelper:

    def __init__(self):
        self.dbstring = settings.dbstring
        # connection to DB server
        try:
            self.cnxn = pyodbc.connect(self.dbstring)
        except Exception as e:
            self._logger.error('Connection to IRIS DB failed: {}'.format(e))

        self.cnxn.autocommit = True
        self.cnxn.timeout = 0
        self._client = suds.client.Client(settings.wsdl_url)
        self._logger = logging.getLogger(__name__)
        self.closed_note = "This ticket has been closed by DCU-ENG automation as unworkable. Questions to hostsec@"

    def ticket_finder(self, address_list, service_id):
        """
        Iterates through list of "like" email addresses and returns IIDs for use in closure query
        :return: list of tupels, example: [(33221396, ), (33221383, )]
        """
        incidents = []

        for address in address_list:
            query = "SELECT iris_incidentID FROM [iris].[dbo].[IRISIncidentMain] WITH(NOLOCK)"\
                    "WHERE iris_serviceID = {}"\
                    "AND OriginalEmailAddress LIKE '%@{}' and iris_statusID = 1".format(service_id, address)

            incident = self._iris_db_connect(query)
            if incident:
                incidents.append(incident[0][0])

        return incidents

    def data_pull(self):
        """
        pulls IID and summary line from all open tickets in IRIS Abuse@ queue
        :return:
        """

        incident_dict = {}

        query = """\
                SELECT a.iris_incidentID, a.IncidentDescription, b.note FROM [iris].[dbo].[IRISIncidentMain] a WITH(NOLOCK) \
                JOIN [iris].[dbo].[IRISIncidentNote] b on b.iris_incidentID = a.iris_incidentID \
                WHERE a.iris_groupID = 489 AND a.iris_serviceID = 220 \
                AND a.iris_statusID = 1"""

        incidents = self._iris_db_connect(query)

        for incident in incidents:
            iid = incident[0]
            subject = incident[1]
            body = incident[2]
            incident_dict[iid] = (subject, body)

        return incident_dict

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

    def ticket_move(self, iid, serviceid, eid):
        """
        This function is designed to take in an IRIS Incident ID and a Service ID to move the IID too using an IRIS DB
        stored procedure
        :param iid:
        :param serviceid:
        :param eid:
        :return:
        """

        query = """\
        SET CONCAT_NULL_YIELDS_NULL, ANSI_WARNINGS, ANSI_PADDING ON;
        SET IMPLICIT_TRANSACTIONS OFF;
        DECLARE @b_checkdatepass bit;
        EXEC IRIS_IncidentMainUpdate_sp @n_incidentID = ?, @n_ServiceID = ?, @vc_modifiedBy = 'DCU Abuse cleanup', @n_iris_groupID = 510, @n_iris_employeeID = ?, @b_checkdatepass = @b_checkdatepass output;
        SELECT @b_checkdatepass AS the_output;"""

        params = (iid, serviceid, eid)

        self._iris_db_connect(query, params)

    def ticket_update(self, iid, eid):

        query = """\
            SET CONCAT_NULL_YIELDS_NULL, ANSI_WARNINGS, ANSI_PADDING ON;
            SET IMPLICIT_TRANSACTIONS OFF;
            DECLARE @b_checkdatepass bit;
            EXEC IRIS_IncidentMainUpdate_sp @n_incidentID = ?, @vc_modifiedBy = 'DCU Abuse cleanup', @n_iris_employeeID = ?, @b_checkdatepass = @b_checkdatepass output;
            SELECT @b_checkdatepass AS the_output;"""

        params = (iid, eid)

        self._iris_db_connect(query, params)

    def _iris_db_connect(self, query, params=None):

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

        self.cnxn.close()
