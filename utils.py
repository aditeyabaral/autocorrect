from openie import StanfordOpenIE
import neuralcoref
import spacy

def getResolvedText(text, spacy_nlp_model):
    neuralcoref.add_to_pipe(spacy_nlp_model)
    document = spacy_nlp_model(text)
    return document._.coref_resolved

def getTriplesFromText(text):
    with StanfordOpenIE() as client:
        triples = client.annotate(text)
        return triples