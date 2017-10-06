import re


class List_helper():

    # o-list is a list of tuples, containing iris_id as key and abuse type as value
    def reg_logic(self, o_list, k_list):
        results = []
        for d in o_list:
            for i in k_list:
                if re.match(i, str(d[1])):
                    results.append(d[0])
                    o_list.remove(d)
                else:
                    print 'No Match ' + str(d) + ' on pattern ' + i
        return results, o_list

