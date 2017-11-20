from mock import patch
from nose.tools import assert_equal
from categorizer.iris_helper import IrisHelper

class TestIRISHelper():
    """
    These functions don't return anything and reach out to services we do not control
    """

    """def __init__(self):
        self._ih = IrisHelper()

    @patch.object(IrisHelper, '_iris_db_connect')
    def ticket_finder_test(self):
        address_list = ['sh.baidu.com']
        service_id = '220'
        expected = "SELECT iris_incidentID FROM [iris].[dbo].[IRISIncidentMain] WITH(NOLOCK)"\
                    "WHERE iris_serviceID = 220"\
                    "AND OriginalEmailAddress LIKE '%@sh.baidu.com' and iris_statusID = 1"
        result = self._ih.ticket_finder(address_list, service_id)
        assert_equal(result, expected)


    def data_pull_test(self):
    todo query build test
        pass

    def ticket_close_test(self):
    todo query build test
        pass

    def ticket_move_test(self):
    todo query build test
        pass
    """