import argparse
import json
import spacy

predicate_wordlist = "./wordlists/change_of_state_predicates2.txt" 

def find_change_of_state(sentence, predicate_wordlist=predicate_wordlist):
    with open(predicate_wordlist) as f: 
        predicate_list = [l.strip() for l in f.readlines()]


    for token in sentence : 
        if (token.lemma_ in predicate_list) and token.tag_[0] == "V" and token.dep_ == "ROOT":
            
            return True 

    return False 

    