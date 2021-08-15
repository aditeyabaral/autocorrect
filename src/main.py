import os
import graph
import scoring
import utils
import time
import argparse
import embedding


def readAnswer(filename):
    with open(filename) as f:
        content = f.read().strip()
    return content


def loadModel(model_path, model_type):
    model_path = os.path.abspath(model_path)
    if os.path.isfile(model_path):
        if model_type == "fasttext":
            model = embedding.loadFastTextModel(model_path)
        else:
            model = embedding.loadWord2VecModel(model_path)
    elif os.path.isdir(model_path):
        model = embedding.loadSentenceTransformerModel(model_path)
    else:
        model = embedding.createSentenceTransformerModel(model_path)
    return model


openie_client = utils.getOpenieClient()
parser = argparse.ArgumentParser(
    description="Obtain arguments for AutoCorrect")
parser.add_argument("key_answer_filepath", metavar="KEY_ANSWER_FILEPATH")
parser.add_argument("test_answer_filepath", metavar="TEST_ANSWER_FILEPATH")
parser.add_argument("--model_path", metavar="MODEL_PATH")
parser.add_argument("--model_type", metavar="MODEL_TYPE")
parser.add_argument("--marks", metavar="TOTAL MARKS", default=10, type=float)
args = vars(parser.parse_args())

key_answer = readAnswer(args["key_answer_filepath"])
test_answer = readAnswer(args["test_answer_filepath"])
model = loadModel(args["model_path"], args["model_type"])
total_marks = args["marks"]

key_answer_graph = graph.createGraph(key_answer, "key", openie_client)
test_answer_graph = graph.createGraph(test_answer, "test", openie_client)

start = time.time()
result_marks = scoring.evaluate(
    model, key_answer_graph, test_answer_graph, total_marks)
end = time.time()

print(f"Marks obtained: {result_marks}")
print(f"Time taken to evaluate: {end-start} seconds")
openie_client.__del__()
