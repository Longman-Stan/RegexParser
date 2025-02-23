#!/usr/bin/env python
import sys
import pickle
import graphviz

from regex import *
from regular_expression import *
from nfa import *
from dfa import *
from antlr4 import *
from rGexLexer import rGexLexer
from visitor import Visitor
from rGexParser import rGexParser

def parseRegex(str):
    #print(str)
    stream = InputStream(str)
    lexer  = rGexLexer(stream)
    stream = CommonTokenStream(lexer)
    parser = rGexParser(stream)
    tree = parser.regex()
    printer = Visitor()
    walker = ParseTreeWalker()
    walker.walk(printer,tree)
    return printer.stack.pop()


if __name__ == "__main__":
    valid = (len(sys.argv) == 4 and sys.argv[1] in ["RAW", "TDA"]) or \
            (len(sys.argv) == 3 and sys.argv[1] == "PARSE")
    if not valid:
        sys.stderr.write(
            "Usage:\n"
            "\tpython3 main.py RAW <regex-str> <words-file>\n"
            "\tOR\n"
            "\tpython3 main.py TDA <tda-file> <words-file>\n"
            "\tOR\n"
            "\tpython3 main.py PARSE <regex-str>\n"
        )
        sys.exit(1)

    if sys.argv[1] == "TDA":
        tda_file = sys.argv[2]
        with open(tda_file, "rb") as fin:
            parsed_regex = pickle.loads(fin.read())
    else:
        regex_string = sys.argv[2]

        # TODO "regex_string" conține primul argument din linia de comandă,
        # șirul care reprezintă regexul cerut. Apelați funcția de parsare pe el
        # pentru a obține un obiect RegEx pe care să-l stocați în
        # "parsed_regex"
        #
        # Dacă nu doriți să implementați parsarea, puteți ignora această parte.
        parsed_regex = parseRegex(regex_string)
        if sys.argv[1] == "PARSE":
            print(parsed_regex)
            sys.exit(0)

    # În acest punct, fie că a fost parsat, fie citit direct ca obiect, aveți
    # la dispoziție variabila "parsed_regex" care conține un obiect de tip
    # RegEx. Aduceți-l la forma de Automat Finit Determinist, pe care să puteți
    # rula în continuare.
    
    reg_exp = regex_to_reg(parsed_regex)
    nfa = re_to_nfa(reg_exp)
    dfa = nfa_to_dfa(nfa)
    
    
    with open(sys.argv[3], "r") as fin:
        content = fin.readlines()

    for word in content:
        # TODO la fiecare iterație, "word" conținue un singur cuvânt din
        # fișierul de input; verificați apartenența acestuia la limbajul
        # regexului dat și scrieți rezultatul la stdout.
        word=word[:-1]
        print(dfa.check(word))
        pass
