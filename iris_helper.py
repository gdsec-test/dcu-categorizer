import pyodbc

class Iris_helper():

    def __init__(self, dbstring):
        self.dbstring = dbstring
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
                "AND OriginalEmailAddress LIKE '%@" + address + "' and iris_statusID = 1"

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

        cursor = self.cnxn.cursor()
        query = query.strip()
        cursor.execute(query)
        incidents = cursor.fetchall()
        cursor.close()
        self.cnxn.close()

        return incidents


    #ToDo can these two functions be done or do items need to be printed to screen?
    def ticket_close(self):
        #ToDo close tickets with note stating unworkable ticket
        pass

    def ticket_move(self):
        #ToDo update tickets iris_serviceID to whatever the new category is
        pass
