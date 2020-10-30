import utils
import spacy
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

text_ml = "Machine learning is the study of computer algorithms that improve automatically through experience.\
        It is seen as a subset of artificial intelligence.\
        Machine learning algorithms build a mathematical model based on sample data, known as training data, in order to make predictions or decisions without being explicitly programmed to do so.\
        Machine learning algorithms are used in a wide variety of applications, such as email filtering and computer vision, where it is difficult or infeasible to develop conventional algorithms to perform the needed tasks."

text_mito = "The mitochondrion is a double membrane bound organelle found in most eukaryotic organisms.\
            They are also known as the powerhouse of the cell.\
            Some cells in some multicellular organisms may however lack them.\
            A number of unicellular organisms have transformed this into other structures.\
            They take in nutrients breaks them down and creates energy rich molecules for the cells.\
            The biochemical processes of the cell are known as cellular respiration"


text_ml2 = "Machine Learning is a branch of artificial intelligence. Its applications include CV and NLP"

nlp = spacy.load("en_core_web_sm")
resolved_text = utils.getResolvedText(text_ml2, nlp)
triples = utils.getTriplesFromText(resolved_text)
utils.tripleToDataFrame(triples, "before.csv")

triples = utils.reduceTriples(triples)
df = utils.tripleToDataFrame(triples, "after.csv")

G = nx.from_pandas_edgelist(df, "subject", "object",
                            edge_attr="edge", create_using=nx.MultiDiGraph())
pos = nx.spring_layout(G)
nx.draw(G, with_labels=True, node_color='skyblue',
        edge_cmap=plt.cm.Blues, pos=pos)
plt.show()
