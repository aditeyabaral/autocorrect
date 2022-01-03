import os
import argparse
import embedding
from pathlib import Path

def getCorpusFromTrainingFolder(training_data_path):
    document_content = list()
    p = Path(training_data_path).glob('**/*')
    files = [x for x in p if x.is_file()]
    for fname in files:
        with open(fname) as f:
            text = f.read().strip()
            document_content.append(text)
    return "\n".join(document_content)


parser = argparse.ArgumentParser(description="Train Embeddings for AutoCorrect")
parser.add_argument("--dir", "-d", help="Directory containing training data", required=True)
parser.add_argument("--model_path", "-m", help="Path to save model", required=True)
parser.add_argument("--model_type", "-t", help="Model type", choices=["fasttext", "word2vec", "transformer"], required=True)
parser.add_argument("--transformer_model_name", "-trf_name", help="Name of the Transformer model", default="bert")
parser.add_argument("--transformer_model_path", "-trf_path", help="Path to the Transformer model", default="bert-base-cased")
args = parser.parse_args()
print(args)

MODEL_TYPE = args.model_type
MODEL_PATH = args.model_path
TRAINING_DATA_DIR = args.dir
TRANSFORMERT_MODEL_NAME = args.transformer_model_name
TRANSFORMERT_MODEL_PATH = args.transformer_model_path

corpus = getCorpusFromTrainingFolder(TRAINING_DATA_DIR)
if MODEL_TYPE in ["fasttext", "word2vec"]:
    if MODEL_TYPE == "fasttext":
        model = embedding.createFastTextModel(corpus)
    elif MODEL_TYPE == "word2vec":
        model = embedding.createWord2VecModel(corpus)
else:
    with open("corpus.txt", 'w') as f:
        f.write(corpus)
    model = embedding.fineTuneSentenceTransformerModel(
        "corpus.txt", TRANSFORMERT_MODEL_NAME, TRANSFORMERT_MODEL_PATH)
    os.remove("corpus.txt")

model.save(MODEL_PATH)
