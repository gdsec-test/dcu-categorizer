import pyodbc
import os
from settings import config_by_name

settings = config_by_name[os.getenv('sysenv') or 'dev']


class IrisHelper:

    def __init__(self):
        self.dbstring = settings.dbstring
        # connection to DB server
        self.cnxn = pyodbc.connect(self.dbstring)
        self.cnxn.autocommit = True
        self.cnxn.timeout = 0

    def trash_man(self, address):
        """
        Iterates through list of "like" email addresses and returns IIDs for use in closure query
        :return: list of tupels, example: [(33221396, ), (33221383, )]
        """

        query = "SELECT iris_incidentID FROM [iris].[dbo].[IRISIncidentMain] WITH(NOLOCK) " \
                "WHERE iris_groupID in (411) AND iris_serviceID = 228" \
                "AND OriginalEmailAddress LIKE '%@{}' and iris_statusID = 1".format(address)

        cursor = self.cnxn.cursor()
        query = query.strip()
        cursor.execute(query)
        incidents = cursor.fetchall()
        cursor.close()
        self.cnxn.close()

        return incidents

    def data_pull(self):
        """
        pulls IID and summary line from all open tickets in IRIS Abuse@ queue
        :return:
        """
        query = "SELECT iris_incidentID, IncidentDescription FROM [iris].[dbo].[IRISIncidentMain] WITH(NOLOCK) " \
                "WHERE iris_groupID in (411) AND iris_serviceID = 228" \
                "AND iris_statusID = 1"

        incidents = self._iris_db_connect(query)

        return incidents

    # TODO can these two functions be done or do items need to be printed to screen?
    def ticket_close(self):
        # TODO close tickets with note stating unworkable ticket
        pass

    def ticket_move(self, iid, serviceid):
        """
        This function is designed to take in an IRIS Incident ID and a Service ID to move the IID too using an IRIS DB
        stored procedure
        :param iid:
        :param serviceid:
        :return:
        """

        query = """\
        SET CONCAT_NULL_YIELDS_NULL, ANSI_WARNINGS, ANSI_PADDING ON;
        SET IMPLICIT_TRANSACTIONS OFF;
        DECLARE @b_checkdatepass bit;
        EXEC IRIS_IncidentMainUpdate_sp @n_incidentID = ?, @n_ServiceID = ?, @vc_modifiedBy = 'DCU Abuse cleanup', @n_iris_groupID = 510, @n_iris_employeeID = 15550, @b_checkdatepass = @b_checkdatepass output;
        SELECT @b_checkdatepass AS the_output;"""

        params = (iid, serviceid)

        rows = self._iris_db_connect(query, params)
        if rows[0][0]:
            result = True
        else:
            result = False

        return result

    def _iris_db_connect(self, query, params=None):
        cursor = self.cnxn.cursor()
        query = query.strip()
        cursor.execute(query, params)
        data = cursor.fetchall()
        cursor.commit()
        cursor.close()
        self.cnxn.close()
        return data
