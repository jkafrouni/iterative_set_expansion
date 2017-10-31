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

    def annotate(self, text, pipeline='first_pipeline'):
        client = NLPCoreClient(PATH_TO_CORENLP)
        doc = client.annotate(text=text, properties=self.properties[pipeline])
        return doc

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
                    sentences_with_entities.append([' '.join([t.word for t in sentence.tokens])])
            elif relation == 2:
                if helpers.any_two(token.ner == 'LOCATION' for token in sentence.tokens):
                    sentences_with_entities.append([' '.join([t.word for t in sentence.tokens])])
            elif relation == 3:
                if any(token.ner == 'ORGANIZATION' for token in sentence.tokens) and any(token.ner == 'LOCATION' for token in sentence.tokens):
                    sentences_with_entities.append([' '.join([t.word for t in sentence.tokens])])
            elif relation == 4:
                if any(token.ner == 'ORGANIZATION' for token in sentence.tokens) and any(token.ner == 'PERSON' for token in sentence.tokens):
                    sentences_with_entities.append([' '.join([t.word for t in sentence.tokens])])
        return sentences_with_entities

    def run_both_pipelines(self, result, relation):
        if result['preprocessed_content']:
            logger.info('[ANNOTATOR]\t [%s] Annotating %s sentences ... (First pipeline)', result['url'], len(result['preprocessed_content']))
            first_annotated_content = self.annotate(result['preprocessed_content'])
            logger.info('[ANNOTATOR]\t [%s] First pipeline done', result['url'])
            
            selected_sentences = self.select_sentences(result['preprocessed_content'], relation, first_annotated_content)
            
            logger.info('[ANNOTATOR]\t [%s] Annotating %s sentences ... (Second pipeline)', result['url'], len(selected_sentences))
            second_annotated_content = self.annotate(selected_sentences, pipeline='second_pipeline')
            logger.info('[ANNOTATOR]\t [%s] Second pipeline done', result['url'])
            result['annotated_content'] = second_annotated_content # update the doc
            # logger.info('[ANNOTATOR]\t [%s] %s', result['url'], second_annotated_content.tree_as_string())
        else:
            logger.info('[ANNOTATOR]\t [%s] No content, skipping...', result['url'])
    
    def annotate_results(self, results, relation):
        """
        Args:
            - results: list of dicts
            - relation: int from 1 to 4
        Given a list of results from the google query, that have been split into lists of sentences,
        Performs the two CoreNLP pipelines and updates the result dictionnaries with annotated objects
        """
        # with ThreadPool(processes=10) as pool:
        #     for result in results:
        #         pool.apply_async(self.run_both_pipelines, args=(result,relation))
        #     pool.close()
        #     pool.join()

        for result in results:
            self.run_both_pipelines(result,relation)
