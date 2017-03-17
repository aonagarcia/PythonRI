# coding: UTF-8
import re

from functions import wordBigrams, Computing_Weight, find_most_similars_docs, Weight

if __name__ == "__main__":
    db_path = "db/cacm.all"  # Direccion de la base cacm
    docs = []

    db_file = open(db_path)

    match_pattern = re.compile("^\.[A-Z]$")

    doc_start = False

    # Leyendo la base de datos
    for line in db_file:
        line = line.strip()
        if line == ".T":
            doc_start = True
            docs.append("")
        elif match_pattern.match(line):
            if docs[-1] == "":
                docs.pop(-1)
            doc_start = False
        elif doc_start == True:
            docs[-1] += line + " "

    db_file.close()

    # print "Resultados para la Base de Datos CACM"
    docs_indexed, df = wordBigrams(docs)

    # print "Documents with boolean weight"
    docs_with_boolean_weight = Computing_Weight(docs_indexed, df, Weight.BOOLEAN)

    # print "\n" * 3

    # print "Documents with TF weight"
    docs_with_TF_weight = Computing_Weight(docs_indexed, df, Weight.TF)

    # print "\n" * 3

    # print "Documents with TF.IDF weight"
    docs_with_TFIDF_weight = Computing_Weight(docs_indexed, df, Weight.TFIDF)

    # print "\n" * 3

    boolean_similarities = find_most_similars_docs(docs_with_boolean_weight, xrange(3))
    TF_similarities = find_most_similars_docs(docs_with_TF_weight, xrange(3))
    TFIDF_similarities = find_most_similars_docs(docs_with_TFIDF_weight, xrange(3))

    print "Printing documents most similars using wordBigrams"
    for x in xrange(3):
        print "For Document:", docs[x], "\n"
        print "Most similars with Boolean Weight"
        for sim, y in boolean_similarities[x]:
            print "Doc(%d): %s - Sim: %f" % (y, docs[y], sim)

        print

        print "Most similars with TF Weight"
        for sim, y in TF_similarities[x]:
            print "Doc: %s - Sim: %f" % (docs[y+1], sim)

        print

        print "Most similars with TF.IDF Weight"
        for sim, y in TFIDF_similarities[x]:
            print "Doc: %s - Sim: %f" % (docs[y+1], sim)

        print
