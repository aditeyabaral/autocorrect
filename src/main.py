import graph
import scoring
import utils
import sys
import time

# key_answer_file, input_answer_file = sys.argv[1:]

text_ml = "Machine learning is the study of computer algorithms that improve automatically through experience.\
        It is seen as a subset of artificial intelligence.\
        Machine learning algorithms build a mathematical model based on sample data, known as training data, in order to make predictions or decisions without being explicitly programmed to do so.\
        Machine learning algorithms are used in a wide variety of applications, such as email filtering and computer vision, where it is difficult or infeasible to develop conventional algorithms to perform the needed tasks."

# ans_ml = "Machine learning is the study of computer algorithms that improve automatically through experience.\
#         Machine learning algorithms build a mathematical model based on sample data, known as training data, in order to make predictions or decisions without being explicitly programmed to do so.\
#         Machine learning algorithms are used in a wide variety of applications, such as email filtering and computer vision, where it is difficult or infeasible to develop conventional algorithms to perform the needed tasks."

ans_ml = "Machine learning is the study of algorithms that improve through experience.\
        It is a subset of artificial intelligence.\
        Machine learning algorithms build mathematical models based on sample data in order to make predictions or decisions without being explicitly programmed to do so.\
        Machine learning algorithms are used in a wide variety of applications, such as email filtering and computer vision"

text_mito = "The mitochondrion is a double membrane bound organelle found in most eukaryotic organisms.\
            They are also known as the powerhouse of the cell.\
            Some cells in some multicellular organisms may however lack them.\
            A number of unicellular organisms have transformed this into other structures.\
            They take in nutrients breaks them down and creates energy rich molecules for the cells.\
            The biochemical processes of the cell are known as cellular respiration"


text_ml2 = "Machine Learning is a branch of artificial intelligence. Its applications include CV and NLP"

"""with open(key_answer_file) as f:
    key_answer = f.read().strip()

with open(input_answer_file) as f:
    input_answer = f.read().strip()"""

key_answer = text_ml
input_answer = ans_ml
openie_client = utils.getOpenieClient()

key_answer_graph = graph.createGraph(key_answer, "key", openie_client)
input_answer_graph = graph.createGraph(input_answer, "ans", openie_client)

start = time.time()
marks = scoring.evaluate(key_answer_graph, input_answer_graph, 4)
end = time.time()
print(f"Time taken to evaluate: {end-start} seconds")
print((marks))
openie_client.__del__()
