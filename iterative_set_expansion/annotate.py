import logging
import numpy as np

# from multiprocessing.dummy import Pool as ThreadPool # PB: CANNOT USE MULTITHREADING WITH ONLY ONE JAVA PROCESS
from multiprocessing import Pool
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
        self.core_client = NLPCoreClient(PATH_TO_CORENLP)

    def select_sentences(self, text, relation, doc):
        """
        Args:
            - text: list of strings (sentences)
            - relation: int from 1 to 4
            - doc: NLPCore.data.Document
        Given the result of the first pipeline, returns the list of reconstructed (from tokens) sentences 
        that contain the right Entities corresponding to the wanted relation:
            Live_In (1): PERSON and LOCATION
            Located_In (2): two LOCATIONs 
            OrgBased_In (3): ORGANIZATION and LOCATION
            Work_For (4): ORGANIZATION and PERSON
        """
        sentences_with_entities = [] # list of sentences which contain the entities needed
        for sentence in doc.sentences:
            # print('\n', i, '\n', sentence.__str__()) # for debug
            if relation == 1:
                if any(token.ner == 'PERSON' for token in sentence.tokens) and any(token.ner == 'LOCATION' for token in sentence.tokens):
                    sentences_with_entities.append(' '.join([t.word for t in sentence.tokens]))
            elif relation == 2:
                if helpers.any_two(token.ner == 'LOCATION' for token in sentence.tokens):
                    sentences_with_entities.append(' '.join([t.word for t in sentence.tokens]))
            elif relation == 3:
                if any(token.ner == 'ORGANIZATION' for token in sentence.tokens) and any(token.ner == 'LOCATION' for token in sentence.tokens):
                    sentences_with_entities.append(' '.join([t.word for t in sentence.tokens]))
            elif relation == 4:
                if any(token.ner == 'ORGANIZATION' for token in sentence.tokens) and any(token.ner == 'PERSON' for token in sentence.tokens):
                    sentences_with_entities.append(' '.join([t.word for t in sentence.tokens]))
        return sentences_with_entities

    def run_pipeline(self, text, pipeline='first_pipeline', doc_id=''):
        
        logger.info('[ANNOTATOR]\t [doc %s] Annotating %s sentences ... (%s)', doc_id, len(text), pipeline)
        doc = self.core_client.annotate(text=text, properties=self.properties[pipeline], doc_id=doc_id)
        logger.info('[ANNOTATOR]\t [doc %s] %s done', doc_id, pipeline)
        return doc

    def mock_run_pipeline(self, pipeline='second_pipeline', doc_id=''):
        # to use when doc has already been annotate (ie xml already exists), to test the rest of the project
        return self.core_client.mock_annotate(doc_id=doc_id)

    def annotate(self, result, relation):

        if result['preprocessed_content']:
            first_annotated_content = self.run_pipeline(result['preprocessed_content'], doc_id=result['id'])
            selected_sentences = self.select_sentences(result['preprocessed_content'], relation, first_annotated_content)
            if selected_sentences: # do not run launch the second pipeline if no sentences selected
                second_annotated_content = self.run_pipeline(selected_sentences, pipeline='second_pipeline', doc_id=result['id'])
                result['annotated_content'] = second_annotated_content # update the doc
            else:
                logger.info('[ANNOTATOR]\t [doc %s] No Entity of required type found, not running second pipeline', result['id'])
        else:
            logger.info('[ANNOTATOR]\t [%s] No content, skipping...', result['url'])

        # mock test:
        # result['annotated_content'] = self.mock_run_pipeline(pipeline='second_pipeline', doc_id=result['id'])
