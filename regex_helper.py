class ListHelper():

    # iris_incidents is a list of tuples, containing iris_id as key and abuse type as value
    def reg_logic(self, iris_incidents, abuse_keywords):
        results = []
        for iris_subject in iris_incidents:
            if iris_subject[1] in abuse_keywords:
                results.append(iris_subject[0])
                iris_incidents.remove(iris_subject)
        return results, iris_incidents
