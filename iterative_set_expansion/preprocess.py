import nltk

def split_sentences(text):
    """
    Given a paragraph in one single string, 
    splits each sentence and returns a list of strings, one string for each sentence.
    """
    return nltk.tokenize.sent_tokenize(text)
