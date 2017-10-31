

class Extractor:
    
    def __init__(self, desired_relation_id, threshold):

        self.relations = {
            1: {'key': 'Live_In', 'entity_types': ['PERSON','LOCATION']},
            2: {'key': 'Located_In', 'entity_types': ['LOCATION','LOCATION']},
            3: {'key': 'OrgBased_In', 'entity_types': ['ORGANIZATION','LOCATION']},
            4: {'key': 'Work_For', 'entity_types': ['ORGANIZATION','PERSON']}
        }
        self.desired_relation = self.relations[desired_relation_id]
        self.threshold = threshold
    
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
                confidence = float(relation.probabilities[self.desired_relation['key']])
                if confidence > self.threshold and set(self.desired_relation['entity_types']) == set([relation.entities[0].type, relation.entities[1].type]):
                    extracted_relations.append(
                        {'confidence': confidence,
                         'entities': {relation.entities[0].type: relation.entities[0].value, 
                                      relation.entities[1].type: relation.entities[1].value}
                        }
                    )
        return extracted_relations

    def extract_from_results(self, results):
        """
        Args:
            - results: list of dicts, one per scraped page, containing their url, text, annotations
        """
        extracted_relations = []
        for result in results:
            if 'annotated_content' in result:
                extracted_relations += self.extract(result['annotated_content'])
        return extracted_relations
