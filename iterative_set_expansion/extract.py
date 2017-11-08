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
                # if relation: # TODO: vérifier pq il peut y en avoir des vides !
                entity_types_correct = set(self.desired_relation['entity_types']) == set([relation.entities[0].type, relation.entities[1].type])
                if entity_types_correct:
                    confidence = float(relation.probabilities[self.desired_relation['key']])
                    entity_type_1, entity_value_1 = relation.entities[0].type, relation.entities[0].value
                    entity_type_2, entity_value_2 = relation.entities[1].type, relation.entities[1].value
                    
                    new_relation = {'confidence': confidence,
                                    'entities': {entity_type_1: entity_value_1,
                                                 entity_type_2: entity_value_2}}

                    print('=============== EXTRACTED RELATION ===============')
                    print('Sentence: ', ' '.join([t.word for t in sentence.tokens]))
                    print('RelationType: %s | Confidence= %s | EntityType1= %s | EntityValue1= %s | EntityType2= %s | EntityValue2= %s'
                          % (self.desired_relation['key'], confidence, entity_type_1, entity_value_1, entity_type_2, entity_value_2))
                    print('============== END OF RELATION DESC ==============')

                    extracted_relations.append(new_relation)

        return extracted_relations
