import logging
import numpy as np

from resources.NLPCore.NLPCore import NLPCoreClient
from config import PATH_TO_CORENLP
from iterative_set_expansion import helpers

logger = logging.getLogger('iterative_set_expansion')


class Annotator:
    
    def __init__(self):
        self.properties = {
            'first_pipeline': {
                "annotators": "tokenize,ssplit,pos,lemma,ner",
                "ner.useSUTime": "0"
            },
            'second_pipeline': {
                "annotators": "tokenize,ssplit,pos,lemma,ner,parse,relation",
                "parse.model": "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz",
                "ner.useSUTime": "0"
            }
        }

    def annotate(self, text, pipeline='first_pipeline'):
        client = NLPCoreClient(PATH_TO_CORENLP)
        doc = client.annotate(text=text, properties=self.properties[pipeline])
        return doc

    def select_sentences(self, text, relation, doc):
        """
        Given the result of the first pipeline and the original text, 
        returns the list of sentences that contain the right Entities
        corresponding to the wanted relation:
            Live_In (1): PERSON and LOCATION
            Located_In (2): two LOCATIONs 
            OrgBased_In (3): ORGANIZATION and LOCATION
            Work_For (4): ORGANIZATION and PERSON
        """
        sentences_with_entities = [] # list of indexes of sentences which contain the entities needed
        for i,sentence in enumerate(doc.sentences):
            if relation == 1:
                if any(token.ner == 'PERSON' for token in sentence.tokens) and any(token.ner == 'LOCATION' for token in sentence.tokens):
                    sentences_with_entities.append(i)
            elif relation == 2:
                if helpers.any_two(token.ner == 'LOCATION' for token in sentence.tokens):
                    sentences_with_entities.append(i)
            elif relation == 3:
                if any(token.ner == 'ORGANIZATION' for token in sentence.tokens) and any(token.ner == 'LOCATION' for token in sentence.tokens):
                    sentences_with_entities.append(i)
            elif relation == 4:
                if any(token.ner == 'ORGANIZATION' for token in sentence.tokens) and any(token.ner == 'PERSON' for token in sentence.tokens):
                    sentences_with_entities.append(i)
        return list(np.array(text)[sentences_with_entities])

    def annotate_results(self, results, relation):
        for result in results:
            if result['preprocessed_content']:
                
                logger.info('[ANNOTATOR]\t [%s] Annotating %s sentences ... (First pipeline)', result['url'], len(result['preprocessed_content']))
                first_annotated_content = self.annotate(result['preprocessed_content'])
                logger.info('[ANNOTATOR]\t [%s] First pipeline done', result['url'])
                
                selected_sentences = self.select_sentences(result['preprocessed_content'], relation, first_annotated_content)
                
                logger.info('[ANNOTATOR]\t [%s] Annotating %s sentences ... (Second pipeline)', result['url'], len(selected_sentences))
                second_annotated_content = self.annotate(selected_sentences, pipeline='second_pipeline')
                logger.info('[ANNOTATOR]\t [%s] Second pipeline done', result['url'])
                result['annotated_content'] = annotated_content # update the doc
                # logger.info('[ANNOTATOR]\t [%s] %s', result['url'], second_annotated_content.tree_as_string())
            else:
                logger.info('[ANNOTATOR]\t [%s] No content, skipping...', result['url'])

