import re


class ListHelper():

    # iris_incidents is a list of tuples, containing iris_id as key and abuse type as value
    def reg_logic(self, iris_incidents, abuse_keywords):
        results = []
        print iris_incidents
        for incident in iris_incidents:
            iid = incident
            print 'iid' + iid
            subject = incident.get(iid[1])
            print subject
            body = incident.get(iid[2])
            for word in abuse_keywords:
                match = re.search(word, subject)
                if match:
                    results.append(iid)
                    iris_incidents.remove(incident)
                else:
                    match = re.search(word, body)
                    if match:
                        results.append(iid)
                        iris_incidents.remove(incident)
                    else:
                        pass
        return results, iris_incidents
