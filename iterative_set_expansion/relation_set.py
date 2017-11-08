import pandas as pd


class RelationSet:

    def __init__(self, relation_type_id, threshold):
        """
        Stores extracted relations along with their confidence, in self.data.
        Structure of self.data:
        """
        self.data = pd.DataFrame(columns=['relation_type', 'confidence', 'entity_1', 'entity_2'])
        # attention: name of Entity is not consistent between NER and RelationExtractor (PEOPLE vs PERSON)
        self.relations = {
            1: {'key': 'Live_In', 'entity_types': ['PEOPLE','LOCATION']},
            2: {'key': 'Located_In', 'entity_types': ['LOCATION','LOCATION']},
            3: {'key': 'OrgBased_In', 'entity_types': ['ORGANIZATION','LOCATION']},
            4: {'key': 'Work_For', 'entity_types': ['ORGANIZATION','PEOPLE']}
        }
        self.relation_type = self.relations[relation_type_id]['key']
        [self.entity_type_1, self.entity_type_2] = self.relations[relation_type_id]['entity_types']
        self.threshold = threshold
        self.used_queries = pd.DataFrame(columns=['relation_type', 'entity_1', 'entity_2']) # TODO: how to deal with first query ?

    def __repr__(self):
        return self.data.__str__()

    def __len__(self):
        return self.data.__len__()

    def add(self, relation):
        """
        Args:
            - relation: {'confidence': confidence, 'entities': {entity_type_1: entity_1, entity_type_2: entity_2}}
        Adds the new relation to the set if:
            - it's not already in the set
            - or it's in the set with a lower confidence
        """
        entity_value_1 = relation['entities'][self.entity_type_1]
        entity_value_2 = relation['entities'][self.entity_type_2]
        new_confidence = relation['confidence']
        # print('=============== EXTRACTED RELATION ===============')
        # print('Sentence: TODO')
        # print('RelationType: %s | Confidence= %s | EntityType1= %s | EntityValue1= %s | EntityType2= %s | EntityValue2= %s' % (self.relation_type, new_confidence, self.entity_type_1, entity_value_1, self.entity_type_2, entity_value_2))
        # print('============== END OF RELATION DESC ==============')

        # TODO: validate type (before ?) + validate confidence here = better
        if ((self.data['entity_1'] == entity_value_1) & (self.data['entity_2'] == entity_value_2)).any():
            idx = self.data[(self.data['entity_1'] == entity_value_1) & (self.data['entity_2'] == entity_value_2)].index.tolist()
            assert len(idx) == 1
            idx = idx[0]
            current_confidence = self.data.loc[idx, 'confidence']
            if new_confidence > current_confidence:
                self.data.loc[idx] = [self.relation_type, new_confidence, entity_value_1, entity_value_2]
        else:
            self.data.loc[len(self.data)] = [self.relation_type, new_confidence, entity_value_1, entity_value_2]

    def prune(self):
        """Removes relations below threshold"""
        self.data = self.data[self.data['confidence'] > self.threshold]

    def generate_new_query(self):
        """
        Selects a relation that will be used for the next query in main(), which:
            - has not been used for querying yet
            - has an extraction confidence that is highest among the tuples that have not yet been used for querying
        """
        # quick pandas manipulations to get unused relations:
        merged = self.data.merge(self.used_queries, indicator=True, how='outer')
        not_used = merged[merged['_merge'] == 'left_only']
        best_row = not_used.loc[not_used['confidence'].idxmax()]

        new_query = ' '.join(best_row[['entity_1', 'entity_2']])
        self.used_queries.loc[len(self.used_queries)] = best_row[['relation_type', 'entity_1', 'entity_2']]

        return new_query
