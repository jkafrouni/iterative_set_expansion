from iterative_set_expansion import helpers

class Extractor:
    
    def __init__(self, desired_relation_id):

        # warning: name of Entity is not consistent between NER and RelationExtractor (PEOPLE vs PERSON)
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
                entity_types_correct = set(self.desired_relation['entity_types']) == set([relation.entities[0].type, relation.entities[1].type])
                if entity_types_correct:
                    confidence = float(relation.probabilities[self.desired_relation['key']])
                    if confidence == max(float(v) for v in relation.probabilities.values()):
                        entity_type_1, entity_value_1 = relation.entities[0].type, relation.entities[0].value
                        entity_type_2, entity_value_2 = relation.entities[1].type, relation.entities[1].value
                        
                        if self.desired_relation['key'] == 'Located_In':
                            # fix because Located_In contains twice the same EntityType, data structure should be modified...
                            entity_type_1 += '_1'
                            entity_type_2 += '_2'

                        new_relation = {'confidence': confidence,
                                        'entities': {entity_type_1: entity_value_1,
                                                     entity_type_2: entity_value_2}}

                        print('=============== EXTRACTED RELATION ===============')
                        print('Sentence: ', helpers.sentence_to_string(sentence))
                        print('RelationType: %s | Confidence= %s | EntityType1= %s | EntityValue1= %s | EntityType2= %s | EntityValue2= %s'
                              % (self.desired_relation['key'], confidence, entity_type_1, entity_value_1, entity_type_2, entity_value_2))
                        print('============== END OF RELATION DESC ==============')

                        extracted_relations.append(new_relation)

        return extracted_relations
