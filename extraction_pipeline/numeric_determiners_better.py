import argparse
import json
import spacy

# import CoNLLReader class



def find_numeric_determiners(sentence):

    numeric_predeterminers =set(["all"])
    special_determiners = set(["both"])
    all_determiners = numeric_predeterminers | special_determiners


    # extract words as list of strings
    words = [t.text.lower() for t in sentence]

    if set(words) & all_determiners:
        for token in sentence:
            include = False
            if token.text.lower() in special_determiners:
                if token.tag_ == "DT" and token.dep_ == "det":
                    include = True

                if not include:
                    for child in token.children:
                        if child.dep_ == "prep" and child.text.lower() == "of":
                            include = True
                            break


            if not include and token.text.lower() in numeric_predeterminers:
                if token.tag_ == "DT" and token.dep_ == "det":
                    head_token = token.head

                    if head_token.tag_ == "CD":
                        print(sentence)
                        include = True # all three of the children
                    else :
                        for child in head_token.children:
                            if child.tag_ == "CD" and token.dep_ == "nummod":
                                print(sentence)
                                include = True # all three children
                                break
                elif token.tag_ == "DT":
                    for child in token.children:
                        if child.dep_ == "prep" and child.text.lower() == "of":
                            for child_child in child.children:
                                if child_child.dep_ == "pobj":
                                    has_det = False
                                    has_nummod = False
                                    for child_child_child in child_child.children:
                                        if (child_child_child.tag_ == "CD"
                                            and child_child_child.dep_ == "nummod"):
                                            has_nummod = True # all of the three children
                                        if (child_child_child.tag_ == "DT"
                                            and child_child_child.dep_ == "det"):
                                            has_det = True # all of the three children

                                    include = has_det and has_nummod
                                    if include:
                                        print(sentence)
                                        break
                            if include:
                                break


    return include


