from math import log, sqrt

import nltk
import re


def enum(**enums):
    return type('Enum', (), enums)

Weight = enum(BOOLEAN=0, TF=1, TFIDF=2)

def postTagging(docs):
    documents = []
    df = {}
    for text in docs:
        tokens = nltk.word_tokenize(text.lower())
        tags = nltk.pos_tag(tokens)

        documents.append({})
        distinctTag = []
        for tag in tags:
            # Dejo solo aquellos terminos que son palabras con al menos dos letras
            if not re.match("^[a-z\-]{2,}$", tag[0]):
                continue

            documents[-1][tag] = documents[-1].get(tag,0) + 1

            if tag not in distinctTag:
                distinctTag.append(tag)

        # if len(documents[-1]) == 0:
        #     documents.pop()

        for tag in distinctTag:
            df[tag] = df.get(tag, 0) + 1

    return documents, df

def wordBigrams(docs):
    documents = []
    df = {}
    stemmer = nltk.stem.PorterStemmer()

    for text in docs:
        tokens = [token for token in nltk.word_tokenize(text.lower()) if re.match("^[a-z\-]{2,}$", token)]

        documents.append({})
        distinctTag = []
        for i in range(1, len(tokens)):
            tag = stemmer.stem(tokens[i-1]) + "-" + stemmer.stem(tokens[i])

            documents[-1][tag] = documents[-1].get(tag,0) + 1

            if tag not in distinctTag:
                distinctTag.append(tag)

        # if len(documents[-1]) == 0:
        #     documents.pop()

        for tag in distinctTag:
            df[tag] = df.get(tag, 0) + 1

    return documents, df

# Procesamiento que se le va a hacer a  la base
def Procesing_Docs(docs):
    df = {}
    documents = []
    stemmer = nltk.stem.PorterStemmer()
    for text in docs:
        tokens = nltk.word_tokenize(text)
        distint_words = []
        documents.append({})
        for token in tokens:
            token = token.lower()
            # Dejo solo aquellos terminos que son palabras con al menos dos letras
            if not re.match("^[a-z]{2,}$", token):
                continue

            token = stemmer.stem(token)

            documents[-1][token] = documents[-1].get(token, 0) + 1

            if token not in distint_words:
                distint_words.append(token)

        # if len(documents[-1]) == 0:
        #     documents.pop()

        # Contador de la frecuencia de documento
        for token in distint_words:
            df[token] = df.get(token, 0) + 1

    return documents, df


def Computing_Weight(docs, df, weighting_eschema):
    if weighting_eschema != Weight.TF:
        modified_documents = []
        for doc in docs:

            modified_documents.append({})

            for term in doc.keys():

                if weighting_eschema == Weight.BOOLEAN:

                    modified_documents[-1][term] = 1


                elif weighting_eschema == Weight.TFIDF:
                    N = float(len(docs))
                    modified_documents[-1][term] = doc[term] * log(N / df[term])

        return modified_documents

    else:
        return docs


def Printing_Matrix(docs, df):
    terms = df.keys()
    terms.sort()

    print "\t".join(terms)

    for doc in docs:
        weights = []
        for term in terms:
            weights.append(str(doc.get(term, 0)))

        print "\t".join(weights)


def Cosine_similarity(doc1, doc2):
    dot_product = 0.0

    norm_doc1 = 0.0
    norm_doc2 = 0.0

    for term in doc1.keys():
        dot_product += doc1[term] * doc2.get(term, 0)
        norm_doc1 += doc1[term] ** 2

    for term in doc2.keys():
        norm_doc2 += doc2[term] ** 2

    return dot_product / sqrt(norm_doc1 * norm_doc2)


def find_most_similars_docs(docs, idx):
    similarities = {id: [] for id in idx}

    for id in idx:
        for idx_doc in xrange(len(docs)):
            if id != idx_doc and docs[id] and docs[idx_doc]:
                sim = Cosine_similarity(docs[id], docs[idx_doc])
                similarities[id].append((sim, idx_doc))

    for id in idx:
        similarities[id].sort(key=lambda x: x[0], reverse=True)
        similarities[id] = similarities[id][:5]
    return similarities