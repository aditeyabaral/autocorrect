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


def loadModel(model_path):
    '''
    if model_path exists, load that model (detect automatically the type), else call createSentenceTransformerModel(model_path)
    '''
    pass


openie_client = utils.getOpenieClient()
parser = argparse.ArgumentParser(
    description="Obtain arguments for AutoCorrect")
parser.add_argument("key_answer_filepath", metavar="KEY_ANSWER_FILEPATH")
parser.add_argument("test_answer_filepath", metavar="TEST_ANSWER_FILEPATH")
parser.add_argument("--model_path", metavar="MODEL_PATH")
parser.add_argument("--marks", metavar="TOTAL MARKS", default=10, type=float)
args = vars(parser.parse_args())

key_answer = readAnswer(args["key_answer_filepath"])
test_answer = readAnswer(args["test_answer_filepath"])
model = loadModel(args["model_path"])
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
