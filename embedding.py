from gensim.models import FastText, Word2Vec
from nltk.tokenize import word_tokenize, sent_tokenize


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


def getSentenceEmbedding(document, model, mode):
    if mode == "average":
        words = word_tokenize(document)
        avg_embedding, counter = 0, 0
        for w in words:
            try:
                avg_embedding += model.wv.get_vector(w)
                counter += 1
            except:
                pass
        return avg_embedding/counter

    else:
        '''Add weighted average here'''
        pass
