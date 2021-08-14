import re
from gensim.models.fasttext import FastText
from gensim.models.word2vec import Word2Vec
import neuralcoref
import numpy as np
import pandas as pd
import embedding
from nltk.corpus import stopwords
from openie import StanfordOpenIE

stopw = stopwords.words("english")


def preprocessText(text, lower=False):
    text = re.sub(r"[^A-Za-z0-9\!\.\?\$\%]", " ", text)
    # text = re.sub(r"\(.*\)", "", text)
    text = re.sub(r" +", " ", text)
    text = re.sub("\n+", "\n", text)
    if lower:
        text = text.lower()
    return text


def roundMarks(x):
    temp = round(x, 2)
    x = str(temp)
    fraction = 0.0
    whole = x
    decimal_postion = x.find(".")
    if decimal_postion != -1:
        whole = int(x[:decimal_postion])
        fraction = int(x[decimal_postion + 1:])
        if fraction != 0:
            if fraction >= 50:
                whole += 1
                fraction = 0
            else:
                fraction = 0.5
    number = whole + fraction
    return number


def getResolvedText(text, spacy_nlp_model):
    if "neuralcoref" not in spacy_nlp_model.pipe_names:
        neuralcoref.add_to_pipe(spacy_nlp_model)
    document = spacy_nlp_model(text)
    return document._.coref_resolved


def getOpenieClient():
    return StanfordOpenIE()


def getTriplesFromText(text, client):
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
                    if (
                        temp_triple["object"] in t["object"]
                        or t["object"] in temp_triple["object"]
                    ):
                        reduced_triples[index]["object"] = max(
                            reduced_triples[index]["object"], t["object"]
                        )
                    else:
                        to_append = True
        else:
            to_append = True

        if to_append:
            reduced_triples.append(t)
            sub_edge_covered.append((subject, edge))

    return reduced_triples


def getFilteredTriples(triples):
    filtered_triples = []
    test_list = sorted(list((" ".join(triple.values()), triple)
                       for triple in triples))
    for i in range(len(test_list)):
        if not any(test_list[i][0] in sub[0] for sub in test_list[i + 1:]):
            filtered_triples.append(test_list[i][1])
    return filtered_triples


def getSimilarity(p1, p2, model):
    if isinstance(model, FastText) or isinstance(model, Word2Vec):
        v1 = embedding.getSentenceEmbeddingFromWordEmbedding(p1, model)
        v2 = embedding.getSentenceEmbeddingFromWordEmbedding(p2, model)
    else:
        v1 = embedding.getSentenceTransformerEmbedding(p1, model)
        v2 = embedding.getSentenceTransformerEmbedding(p2, model)

    cosine_similarity = np.dot(
        v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    return cosine_similarity
