from gensim.models import FastText, Word2Vec
from nltk.tokenize import word_tokenize, sent_tokenize
import numpy as np


def getSimilarityBetweenVector(vector1, vector2):
    return np.dot(vector1, vector2)/(np.linalg.norm(vector1)*np.linalg.norm(vector2))


def getSimilarityBetweenText(text1, text2, model):
    vector1 = getSentenceEmbedding(text1, model)
    vector2 = getSentenceEmbedding(text2, model)
    return getSimilarityBetweenVector(vector1, vector2)


def createFastTextModel(corpus):
    sentences = sent_tokenize(corpus)
    train = list(map(word_tokenize, sentences))
    model = FastText(min_count=1, size=200)
    model.build_vocab(sentences=train)
    model.train(sentences=train,
                total_examples=ft_model.corpus_count, epochs=20)
    return model


def createWord2VecModel(corpus):
    sentences = sent_tokenize(corpus)
    train = list(map(word_tokenize, sentences))
    model = Word2Vec(min_count=1, size=200)
    model.build_vocab(sentences=train)
    model.train(sentences=train,
                total_examples=ft_model.corpus_count, epochs=20)
    return model


def createEmbeddingModel(corpus, mode="fastText"):
    if mode == "word2vec":
        model = createWord2VecModel(corpus)
    else:
        model = createFastTextModel(corpus)
    return model


def getSentenceEmbedding(document, model, mode="average"):
    if mode == "average":
        words = word_tokenize(document)
        avg_embedding = np.zeros(len(model.wv[0]))
        counter = 1
        for w in words:
            try:
                avg_embedding += model.wv.get_vector(w)
                counter += 1
            except:
                pass
        return avg_embedding/counter

    else:
        '''Add weighted average here'''
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
