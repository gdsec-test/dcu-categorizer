import re


class List_helper():

    # o-list is a list of tuples, containing iris_id as key and abuse type as value
    def reg_logic(self, o_list, k_list):
        results = []
        for d in o_list:
            if d[1] in k_list:
                print '{} is in {}'.format(d, k_list)
                results.append(d[0])
                o_list.remove(d)
            else:
                print 'No Match {} on pattern {}'.format(str(d), k_list)
        return results, o_list

