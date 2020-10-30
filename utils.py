import re
from openie import StanfordOpenIE
from nltk.corpus import stopwords
import neuralcoref
import spacy
import pandas as pd

stopw = stopwords.words("english")

def preprocessText(text, lower=False):
    text = re.sub(r"[^A-Za-z0-9\!\.\?\$\%]". " ", text)
    #text = re.sub(r"\(.*\)", "", text)
    text = re.sub(r" +", " ", text)
    text = re.sub("\n+", "\n", text)
    if lower:
        text = text.lower()
    return text

def getResolvedText(text, spacy_nlp_model):
    neuralcoref.add_to_pipe(spacy_nlp_model)
    document = spacy_nlp_model(text)
    return document._.coref_resolved


def getTriplesFromText(text):
    with StanfordOpenIE() as client:
        triples = client.annotate(text)
        return triples

def tripleToDataFrame(triples, name):
    df = pd.DataFrame()
    subject, relation, predicate = list(), list(), list()
    for t in triples:
        subject.append(t["subject"])
        relation.append(t["relation"])
        predicate.append(t["object"])
    df["subject"] = subject
    df["edge"] = relation
    df["object"] = predicate
    df.to_csv(name)
    return df

def reduceTriples(triples):
    filtered_triples = list()
    for t in triples:
        subject = t["subject"].split()
        if len(subject) == 1 and subject[0] in stopw:
            continue
        else:
            filtered_triples.append(t)

    reduced_triples = list()
    sub_edge_covered = list()
    to_append = True
    for t in filtered_triples:
        subject = t["subject"]
        edge = t["relation"]
        to_append = False
        if (subject, edge) in sub_edge_covered:
            for index, temp_triple in enumerate(reduced_triples):
                if (temp_triple["subject"], temp_triple["relation"]) == (subject, edge):
                    if temp_triple["object"] in t["object"] or t["object"] in temp_triple["object"]:
                        reduced_triples[index]["object"] = max(reduced_triples[index]["object"], t["object"])
                    else:
                        to_append = True
        else:
            to_append = True
        if to_append:
            reduced_triples.append(t)
            sub_edge_covered.append((subject, edge))
    return reduced_triples

def getFilteredTriples(text):
    triples = getTriplesFromText(text)
    filtered_triples = []
    test_list = []
    for triple in triples:
        check_string = " ".join(triple.values)
        if not any(check_string in sub for sub in test_list):
            test_list.append(check_string)
            filtered_triples.append(triple)
    return filtered_triples
