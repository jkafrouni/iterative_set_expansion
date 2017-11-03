from pprint import pprint # for tests

class Extractor:
    
    def __init__(self, desired_relation_id):

        # attention: name of Entity is not consistent between NER and RelationExtractor (PEOPLE vs PERSON)
        self.relations = {
            1: {'key': 'Live_In', 'entity_types': ['PEOPLE','LOCATION']},
            2: {'key': 'Located_In', 'entity_types': ['LOCATION','LOCATION']},
            3: {'key': 'OrgBased_In', 'entity_types': ['ORGANIZATION','LOCATION']},
            4: {'key': 'Work_For', 'entity_types': ['ORGANIZATION','PEOPLE']}
        }
        self.desired_relation = self.relations[desired_relation_id]
    
    def extract(self, doc):
        """
        Args:
            - doc: NLPCore.data.Document
        Given an annotated document doc, returns the list of relations above the desired threshold
        We make sure that the relations are between entities of the correct type
        """
        extracted_relations = []
        for sentence in doc.sentences:
            for relation in sentence.relations:
                if relation: # TODO: vérifier pq il peut y en avoir des vides !
                    if set(self.desired_relation['entity_types']) == set([relation.entities[0].type, relation.entities[1].type]):
                        extracted_relations.append(
                            {'confidence': float(relation.probabilities[self.desired_relation['key']]),
                             'entities': {relation.entities[0].type: relation.entities[0].value, 
                                          relation.entities[1].type: relation.entities[1].value}
                            }
                        )
        return extracted_relations
