# coding: UTF-8
import re

from functions import postTagging, Computing_Weight, find_most_similars_docs, Weight

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

    print (docs[0])
    print (docs[1])

    print (docs[52])
    print (docs[96])
    print (docs[195])
    print (docs[132])
    print (docs[145])
    print (docs[154])
    print (docs[1075])

    # Recommendations of the SHARE ALGOL Committee
    # Signal Corps Research and Development on Automatic Programming of Digital Computers
    # Report on the Algorithmic Language ALGOL 60
    # Riccati-Bessel Functions of First And Second Kind (Algorithm 22)
    # The Use of Computers in Engineering Classroom Instruction
    # Trie Memory
    # Multiple Integration (Algorithm 146)