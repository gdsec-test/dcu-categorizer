import pyodbc
from settings import devdbstring

def test_query(iid, serviceid, groupid, eid):

    # connection to DB server
    cnxn = pyodbc.connect(devdbstring)
    cnxn.autocommit = True
    cnxn.timeout = 0

    query = """\
    SET CONCAT_NULL_YIELDS_NULL, ANSI_WARNINGS, ANSI_PADDING ON;
    DECLARE @b_checkdatepass bit;
    EXEC IRIS_IncidentMainUpdate_sp @n_incidentID = ?, @n_ServiceID = ?, @vc_modifiedBy = 'DCU Abuse cleanup', @n_iris_groupID = ?, @n_iris_employeeID = ?, @b_checkdatepass = @b_checkdatepass output;
    SELECT * FROM irisincidentmain WHERE iris_incidentid = """ + iid + """;"""

    params = (iid, serviceid, groupid, eid)
    cursor = cnxn.cursor()
    query = query.strip()
    cursor.execute(query, params)
    print cursor.fetchall()
    cursor.close()
    cnxn.close()


if __name__ == '__main__':
    iid = '1354878'
    serviceid = '212' # 212 phishing, 220 DS Abuse
    groupid = '510'
    eid = '19043'
    print test_query(iid, serviceid, groupid, eid)
