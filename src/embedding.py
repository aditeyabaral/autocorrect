import numpy as np
from gensim.models import FastText, Word2Vec
from nltk.tokenize import word_tokenize, sent_tokenize
from simpletransformers.language_modeling import LanguageModelingModel
from sentence_transformers import SentenceTransformer, models

def loadFastTextModel(model_path):
    model = FastText.load(model_path)
    return model


def loadWord2VecModel(model_path):
    model = Word2Vec.load(model_path)
    return model


def createFastTextModel(corpus):
    sentences = sent_tokenize(corpus)
    train = list(map(word_tokenize, sentences))
    model = FastText(min_count=1, size=200)
    model.build_vocab(sentences=train)
    model.train(sentences=train, total_examples=model.corpus_count, epochs=20)
    return model


def createWord2VecModel(corpus):
    sentences = sent_tokenize(corpus)
    train = list(map(word_tokenize, sentences))
    model = Word2Vec(min_count=1, size=200)
    model.build_vocab(sentences=train)
    model.train(sentences=train, total_examples=model.corpus_count, epochs=20)
    return model


def createWordEmbeddingModel(corpus, mode="fastText"):
    if mode == "word2vec":
        model = createWord2VecModel(corpus)
    else:
        model = createFastTextModel(corpus)
    return model


def getSentenceEmbeddingFromWordEmbedding(document, model, mode="average"):
    if mode == "average":
        words = word_tokenize(document)
        avg_embedding = np.zeros(len(model.wv["test"]))
        counter = 1
        for w in words:
            try:
                avg_embedding += model.wv.get_vector(w)
                counter += 1
            except:
                pass
        return avg_embedding / counter

    else:
        """Add weighted average here"""  # finish this
        # sentence_set = []
        # for sentence in sentence_list:
        #     vs = np.zeros(embedding_size)
        #     sentence_length = 1
        #     for word in word_tokenize(sentence):
        #         try:
        #             vs = np.add(vs, wordvec_func(word))
        #             sentence_length += 1
        #         except:
        #             pass
        #
        #     vs = np.divide(np.nan_to_num(vs), sentence_length)
        #     sentence_set.append(vs)
        #
        # pca = PCA()
        # pca.fit(np.array(sentence_set))
        # u = pca.components_[0]
        # u = np.multiply(u, np.transpose(u))
        #
        # if len(u) < embedding_size:
        #     for i in range(embedding_size - len(u)):
        #         u = np.append(u, 0)
        #
        # sentence_vecs = []
        # for vs in sentence_set:
        #     sub = np.multiply(u, vs)
        #     sentence_vecs.append(np.subtract(vs, sub))
        #
        # return sentence_vecs
        pass


def loadSentenceTransformerModel(model_path):
    sentence_transformer_model = SentenceTransformer(model_path)
    return sentence_transformer_model


def createSentenceTransformerModel(model_type="paraphrase-MiniLM-L12-v2"):
    # https://www.sbert.net/docs/pretrained_models.html
    sentence_transformer_model = SentenceTransformer(model_type)
    return sentence_transformer_model


def getSentenceTransformerEmbedding(sentence, model):
    sentence_embeddings = model.encode([sentence])
    return sentence_embeddings[0]


def fineTuneEmbeddingLayer(train_text_path, model_type, model_name):
    training_args = {
        "reprocess_input_data": True,
        "overwrite_output_dir": True,
        "block_size": 512,
        "max_seq_length": 512,
        "learning_rate": 5e-6,
        "train_batch_size": 8,
        "gradient_accumulation_steps": 8,
        "num_train_epochs": 3,
        "mlm": True,
        "output_dir": "fine-tuned-embeddings",
    }

    model = LanguageModelingModel(model_type, model_name, args=training_args)
    model.train_model(train_text_path)


def fineTuneSentenceTransformerModel(train_text_path, model_name="bert", model_path="bert-base-cased"):
    fineTuneEmbeddingLayer(
        train_text_path, model_name, model_path)
    embedding_model = models.Transformer("fine-tuned-embeddings")
    # add tokens?
    pooling_model = models.Pooling(embedding_model.get_word_embedding_dimension(),
                                   pooling_mode_mean_tokens=True,
                                   pooling_mode_cls_token=False,
                                   pooling_mode_max_tokens=False)
    model = SentenceTransformer(modules=[embedding_model, pooling_model])
    return model