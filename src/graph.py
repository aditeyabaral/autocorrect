import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import spacy
import utils

nlp = spacy.load("en_core_web_sm")


def createGraph(text, fn, openie_client):
    resolved_text = utils.getResolvedText(text, nlp)
    triples = utils.getTriplesFromText(resolved_text, openie_client)
    utils.tripleToDataFrame(triples, f"{fn}_before.csv")

    triples = utils.getFilteredTriples(triples)
    triples = utils.reduceTriples(triples)
    df = utils.tripleToDataFrame(triples, f"{fn}_after.csv")

    G = nx.from_pandas_edgelist(
        df, "subject", "object", edge_attr="edge", create_using=nx.MultiDiGraph()
    )
    return G


def displayGraph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, with_labels=True, node_color="skyblue", edge_cmap=plt.cm.Blues, pos=pos)
    plt.show()
