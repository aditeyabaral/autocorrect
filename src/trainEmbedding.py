import os
import argparse
import embedding


def getCorpusFromTrainingFolder(training_data_path):
    document_content = list()
    # for each file in this training_data_path folder
    # if pdf/txt/doc/docx -> extract text
    # append to document_content
    return ". ".join(document_content)


parser = argparse.ArgumentParser(
    description="Create Embedding Model for AutoCorrect")
parser.add_argument("training_data_path", metavar="TRAINING_DATA_PATH")
parser.add_argument("model_path", metavar="MODEL_PATH")
parser.add_argument("model_type", metavar="MODEL_TYPE")
parser.add_argument("--tf_model_type",
                    metavar="TRANSFORMER_MODEL_TYPE", default="bert")
parser.add_argument(
    "--tf_model_name", metavar="TRANSFORMER_MODEL_NAME", default="bert-base-cased")
args = vars(parser.parse_args())

model_type = args["model_type"].lower()
training_data_path = args["training_data_path"]
model_path = args["model_path"]
corpus = getCorpusFromTrainingFolder(training_data_path)

if model_type in ["fasttext", "word2vec"]:
    if model_type == "fasttext":
        model = embedding.createFastTextModel(corpus)
    elif model_type == "word2vec":
        model = embedding.createFastTextModel(corpus)
else:
    with open("corpus.txt", 'w') as f:
        f.write(corpus)
    tf_model_type = args["tf_model_type"]
    tf_model_name = args["tf_model_name"]
    model = embedding.fineTuneSentenceTransformerModel(
        "corpus.txt", tf_model_type, tf_model_name)
    os.remove("corpus.txt")

model.save(model_path)
