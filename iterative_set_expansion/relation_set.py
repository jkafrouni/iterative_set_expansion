

class RelationSet:

    def __init__(self, desired_relation_id):
        """
        Stores extracted relations along with their confidence, in self.data.
        Structure of self.data:
            {
                ...
                {entity_type_1: entity_1, entity_type_2: entity_2}: confidence,
                ...
            }
        """
        self.data = dict()
        self.relations = {
            1: {'key': 'Live_In', 'entity_types': ['PERSON','LOCATION']},
            2: {'key': 'Located_In', 'entity_types': ['LOCATION','LOCATION']},
            3: {'key': 'OrgBased_In', 'entity_types': ['ORGANIZATION','LOCATION']},
            4: {'key': 'Work_For', 'entity_types': ['ORGANIZATION','PERSON']}
        }
        self.desired_relation = self.relations[desired_relation_id]

    def add(self, relation):
        """
        Args:
            - relation: {'confidence': confidence, 'entities': {entity_type_1: entity_1, entity_type_2: entity_2}}
        Adds the new relation to the set if:
            - it's not already in the set
            - or it's in the set with a lower confidence
        """
        if relation['entities'] not in self.data:
            self.data[relation['entities']] = relation['confidence']
        else:
            current_confidence= self.data[relation['entities']]
            new_confidence = self.relation['confidence']
            self.data.update({relation['entities']: max(current_confidence, new_confidence)})

    def __repr__(self):
        return self.data.__str__()

    def __len__(self):
        return self.data.__len__()
