import spacy 
from spacy import displacy
from spacy.matcher import PhraseMatcher

implicative_path = "wordlists/implicative_predicates.txt"

def find_implicatives(sentence, impl_pred_path=implicative_path):
    
    nlp = spacy.load("en_core_web_sm")
    matcher = PhraseMatcher(nlp.vocab)
    
    with open(impl_pred_path, 'r') as f:
        implicatives = [l.strip() for l in f]
        implicative_pairs = [item.split(":") for item in implicatives] #seperate predicates and inferences
        implicative_predicates = [pair[0] for pair in implicative_pairs]
        implicative_inferences_dict = {pair[0]:pair[1] for pair in implicative_pairs} #dictionary mapping predicates to inferences
        implicative_verbs = set([p.split()[0] for p in implicative_predicates])
        # add implicative predicates to matcher
        patterns = [nlp.make_doc(text) for text in implicative_predicates]
        matcher.add("IMPL_PRED_LIST", None, *patterns)
        

    #words = [t.text for t in sentence]
    # find matches of implicative predicates in the sentence
    matches = matcher(sentence)

    if len(matches) > 0:
        for match_id, start, end in matches:
            impl_phrase = sentence[start:end]
            #print(str(impl_phrase))
        # match found, proceed to further checking
        for token in sentence:
            if (str(token) in implicative_verbs
                and token.tag_[0] == "V"
                and token.dep_ == "ROOT"):
                #include = False
                for child in token.children:
                    if child.dep_ == "prep":
                        for childs in child.children:
                            if childs.dep_ == "pcomp" and childs.pos_ == "VERB":
                                return True 
                                #include = True
                                #break
                    else:
                        if child.dep_ == "xcomp" and child.pos_ == "VERB":
                            return True 
                            #include = True
                            #break
    return False 