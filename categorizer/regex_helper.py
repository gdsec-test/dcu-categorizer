import re


class ListHelper:

    # iris_incidents is a list of tuples, containing iris_id as key and abuse type as value
    def reg_logic(self, iris_incidents, abuse_keywords):
        results = []
        for incident, (subject, body) in iris_incidents.items():
            for word in abuse_keywords:
                match = re.search(word, subject, re.IGNORECASE)
                if match:
                    results.append(incident)
                    iris_incidents.pop(incident)
                    break
                else:
                    match = re.search(word, body, re.IGNORECASE)
                    if match:
                        results.append(incident)
                        iris_incidents.pop(incident)
                        break

        return results, iris_incidents
