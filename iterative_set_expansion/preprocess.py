import nltk

def split_sentences(text):
    """
    Given a paragraph in one single string, 
    splits each sentence and returns a list of strings, one string for each sentence.
    """
    sentences = nltk.tokenize.sent_tokenize(text)
    while '' in sentences: # quick fix, nltk might add empty sentences
        sentences.remove('')
    return sentences