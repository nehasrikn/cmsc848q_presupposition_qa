import json 
from pyserini.search.faiss import FaissSearcher 
import sys

# credits: Maharshi Gor
def get_document_info(searcher, result):
    docid = result.docid
    text = searcher.doc(docid).raw()
    content = json.loads(text)['contents']
    title = content.split('\n', 1)[0]
    if title[0] == '"':
        title = title[1:-1]

    return {'docid': docid, 'title':title, 'content': content}


def run_dpr(question, searcher): 
    paragraphs = []
    results = searcher.search(question)
    for elem in results: 
        doc_dict = get_document_info(searcher, elem)
        paragraphs.append(doc_dict)
    
    return paragraphs

def save_results(input_filepath, output_filepath, searcher): 
    queries = []
    with open(input_filepath) as fp : 
        for line in fp: 
            queries.append(line.strip())

    print(f"loaded {len(queries)} queries")
    with open(output_filepath, "w") as f:
        for elem in queries: 
            doc = {}
            paragraphs = run_dpr(elem, searcher)
            doc = {
                "question": elem,
                "passages": paragraphs
            }
            s = json.dumps(doc)
            print(type(s)) 
            f.write(f"{s}\n")


    print("done")

if __name__ == "__main__": 
    searcher = FaissSearcher.from_prebuilt_index(
    'wikipedia-dpr-single-nq-bf',
    'facebook/dpr-question_encoder-multiset-base'
    )

    input_filename = "questions.txt"
    output_filename = "questions_top10_.jsonl"

    save_results(input_filename, output_filename, searcher)




    
    

    
