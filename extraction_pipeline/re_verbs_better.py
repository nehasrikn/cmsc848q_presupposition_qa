re_verbs_corpus = "wordlists/re_verbs_updated.txt"

def find_re_verbs(sentence, cos_predicate_path = re_verbs_corpus):

    with open(cos_predicate_path, 'r') as f:
        re_verbs = set([l.strip() for l in f.readlines()])

    # extract words as list of strings
    words = [t.text for t in sentence]
    
    if set(words) & re_verbs:
        
        for token in sentence:
            print(token, token.tag_, token.dep_)
            if (str(token) in re_verbs
                and token.tag_[0] == "V"
                and token.dep_ == "ROOT"): ## why does the verb have 
                
                if len(list(token.children))  > 0: 
                    return True 
                    
    return False 


# "holly decided to rebook the flight" > does not work, why? 

    