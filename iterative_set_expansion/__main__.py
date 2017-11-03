#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Columbia University
COMS 6111 - Advanced Database Systems (Fall 2017)
Project 2
Author: Jerome Kafrouni

Implementation of an information extraction system that uses Iterative Set Expansion
over search results returned by Google, parsed with BeautifulSoup 
and processed with Stanford CoreNLP and Stanford Relation Extractor
"""
import sys
import logging
import threading
import os

from iterative_set_expansion import helpers
from iterative_set_expansion import query
from iterative_set_expansion import scrape
from iterative_set_expansion import preprocess
from iterative_set_expansion import annotate
from iterative_set_expansion import extract
from iterative_set_expansion import relation_set
from tests import mock_query_and_scraping

logger = logging.getLogger('iterative_set_expansion')
logger.propagate = False # do not log in console
os.makedirs('logs', exist_ok=True) # create directory for logs if it's not there already
handler = logging.FileHandler('logs/iterative_set_expansion.log')
formatter = logging.Formatter(
    fmt='[%(asctime)s %(levelname)s]\t%(message)s',
    datefmt='%d-%m-%Y %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def main(is_test=True):
    """
    Main routine, 
    Inputs:
        r: int between 1 and 4, for categories Live_In (1), Located_In (2), OrgBased_In (3), Work_For (4)
        t: float between 0 and 1, extraction confidence threshold
        q: string, seed query of plausible tuple
        k: int greater than 0, number of tuples wanted
    Until k tuples are extracted:
        Runs new query (augmented with best new tuple), processes retrieved documents, extracts new tuples.
    """

    try:
        r, t, q, k = helpers.check_arguments(sys.argv[1:]) 
        # check_arguments will raise an error if one of the args is wrong
    except Exception as e:
        print(e)
        return

    logger.info('\n\n ========================================================================\n\n')
    logger.info('[MAIN]\t\t Started with args: r = %s, t = %s, q = %s, k = %s', r, t, q, k)

    helpers.print_arguments(r, t, q, k)

    X = relation_set.RelationSet(r, t) # extracted tuples
    annotator = annotate.Annotator()
    extractor = extract.Extractor(r)

    iteration_number = 0
    while len(X) < k:
        iteration_number += 1
        print('=========== Iteration: %s - Query: %s ===========' %(iteration_number, q))

        # results = query.query_google(q) # TODO: garder juste les URLs ?
        # scrape.add_url_content(q, results) # add 'content' to each doc in results, which is the scraped content of the webpage
        results = mock_query_and_scraping.load_query_results(q) # for tests

        for result in results:
            print('Processing: ', result['url'])
            
            result['preprocessed_content'] = preprocess.split_sentences((result['content']))
            if not result['preprocessed_content']: # to test
                print('No content from this website, no relations extracted (Overall: %s)' % (len(X),))
            
            annotator.annotate(result, r) # updates result
            extracted_relations = []
            if 'annotated_content' in result:
                extracted_relations = extractor.extract(result['annotated_content'])
            
            for extracted_relation in extracted_relations: # TODO: implement append
                X.add(extracted_relation)

            print('Relations extracted from this website: %s (Overall: %s)' % (len(extracted_relations), len(X)))
        
        print('Pruning relations below threshold...')
        X.prune()
        print('Number of tuples after pruning: ', len(X))
        print('================== ALL RELATIONS =================')
        print(X)

        q = X.generate_new_query()
        
        break
          

if __name__ == '__main__':
    main()
