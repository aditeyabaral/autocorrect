import spacy
import utils
import networkx as nx
from matplotlib import cm
import matplotlib.pyplot as plt


nlp = spacy.load("en_core_web_lg")


def createGraph(text, filename, openie_client):
    resolved_text = utils.getResolvedText(text, nlp)
    triples = utils.getTriplesFromText(resolved_text, openie_client)
    _ = utils.tripleToDataFrame(triples, f"{filename}_triples.csv")

    triples = utils.getFilteredTriples(triples)
    triples = utils.reduceTriples(triples)
    df = utils.tripleToDataFrame(triples, f"{filename}_triples_reduced.csv")

    G = nx.from_pandas_edgelist(
        df, "subject", "object", edge_attr="edge", create_using=nx.MultiDiGraph()
    )
    return G


def displayGraph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, with_labels=True, node_color="skyblue",
            edge_cmap=cm.Blues, pos=pos)
    plt.show()
