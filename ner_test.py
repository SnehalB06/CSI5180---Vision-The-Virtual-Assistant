import spacy

nlp = spacy.load('en_core_web_sm')


def getNER(text):
    doc = nlp(text)
    return doc.ents
