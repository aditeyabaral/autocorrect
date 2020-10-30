import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import spacy

import eval
import utils

text_ml = "Machine learning is the study of computer algorithms that improve automatically through experience.\
        It is seen as a subset of artificial intelligence.\
        Machine learning algorithms build a mathematical model based on sample data, known as training data, in order to make predictions or decisions without being explicitly programmed to do so.\
        Machine learning algorithms are used in a wide variety of applications, such as email filtering and computer vision, where it is difficult or infeasible to develop conventional algorithms to perform the needed tasks."

ans_ml = "Machine learning is the study of computer algorithms that improve automatically through experience.\
        It is seen as a subset of artificial intelligence.\
        Machine learning algorithms build a mathematical model based on sample data, known as training data, in order to make predictions or decisions without being explicitly programmed to do so."

text_mito = "The mitochondrion is a double membrane bound organelle found in most eukaryotic organisms.\
            They are also known as the powerhouse of the cell.\
            Some cells in some multicellular organisms may however lack them.\
            A number of unicellular organisms have transformed this into other structures.\
            They take in nutrients breaks them down and creates energy rich molecules for the cells.\
            The biochemical processes of the cell are known as cellular respiration"


nlp = spacy.load("en_core_web_sm")


def createGraph(text, fn):
    resolved_text = utils.getResolvedText(text, nlp)
    triples = utils.getTriplesFromText(resolved_text)
    utils.tripleToDataFrame(triples, f"{fn}_before.csv")

    triples = utils.getFilteredTriples(triples)
    triples = utils.reduceTriples(triples)
    df = utils.tripleToDataFrame(triples, f"{fn}_after.csv")

    G = nx.from_pandas_edgelist(
        df, "subject", "object", edge_attr="edge", create_using=nx.MultiDiGraph()
    )
    return G


G1 = createGraph(text_ml, "key")
G2 = createGraph(ans_ml, "ans")

print(eval.evaluate(G1, G2))
# pos = nx.spring_layout(G)
# nx.draw(G, with_labels=True, node_color='skyblue',
#         edge_cmap=plt.cm.Blues, pos=pos)
# plt.show()
