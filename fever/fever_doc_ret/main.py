# import sys
# sys.path.append('/fs/clip-ml/navita/Projects/HW/cmsc848Q_Project/athene/src/')


import os
import sys
import json
sys.path.append('src/')


from athene.retrieval.document.docment_retrieval import main as document_retrieval_main
from athene.retrieval.sentences.ensemble import entrance as sentence_retrieval_ensemble_entrance

from common.dataset.reader import JSONLineReader
from retrieval.fever_doc_db import FeverDocDB


def doc_retrieval(data_dir, prefix):
    document_k_wiki = 7
    raw_test_set = f'{data_dir}/data/fever/{prefix}.jsonl'
    test_doc_file = f'{data_dir}/output/docs/{prefix}.wiki.7.jsonl'
    document_add_claim = True
    document_parallel = True

    document_retrieval_main(db_path, document_k_wiki, raw_test_set, 
                        test_doc_file, document_add_claim, document_parallel)


    
def get_valid_texts(lines, page):
    if not lines:
        return []
    doc_lines = [doc_line.split("\t")[1] \
                 if len(doc_line.split("\t")[1]) > 1 else "" \
                 for doc_line in lines.split("\n")]
    
    doc_lines = list(zip(doc_lines, [page] * len(doc_lines), range(len(doc_lines))))
    return doc_lines


def sent_retrieval(data_dir, prefix):
    test_doc_file = f'{data_dir}/output/docs/{prefix}.wiki.7.jsonl'
    test_sent_file = f'{data_dir}/output/docs/{prefix}.sent.7.jsonl'
    db = FeverDocDB(db_path)
    
    jlr = JSONLineReader()
    with open(test_doc_file, 'rb') as f:
        lines = jlr.process(f)
        
    outputs = []
    for line in lines:
        pages = set()
        pages.update(page for page in line['predicted_pages'])
        p_lines = []
        dev = []
        indexes = []


        for page in pages:
            doc_lines = db.get_doc_lines(page)
            if not doc_lines:
                continue

            p_lines.extend(get_valid_texts(doc_lines, page))

        for doc_line in p_lines:
            if not doc_line[0]:
                continue
            dev.append(doc_line[0])
            indexes.append([doc_line[1], doc_line[2], doc_line[0], 0])

        outputs.append({"id":line['id'], "claim": line['claim'], "evidence": indexes})
        
    with open(test_sent_file, "w+") as f:
        for line in outputs:
            f.write(json.dumps(line) + "\n")
    
        

def _construct_args_for_sentence_retrieval(phase='training'):
    test_doc_file = f'{data_dir}/output/docs/{prefix}.wiki.7.jsonl'
    test_set_file = f'{data_dir}/output/docs/{prefix}.p7.s5.jsonl'

    fasttext_path = f'{data_dir}/data/fasttext/wiki.en.bin'
    
    sentence_retrieval_ensemble_param = {
        'num_model': 5,
        'random_seed': 1234,
        'tf_random_state': [88, 12345, 4444, 8888, 9999],
        'num_negatives': 5,
        'c_max_length': 20,
        's_max_length': 60,
        'reserve_embed': False,
        'learning_rate': 0.001,
        'batch_size': 512,
        'num_epoch': 20,
        'dropout_rate': 0.1,
        'num_lstm_units': 128,
        'share_parameters': False,
        'model_path': os.path.join(
            f'{data_dir}/models/', 'sentence_retrieval_ensemble')
    }
    
    from argparse import Namespace
    _args = Namespace()
    for k, v in sentence_retrieval_ensemble_param.items():
        setattr(_args, k, v)
    
    setattr(_args, 'train_data', test_doc_file)
    setattr(_args, 'dev_data', test_doc_file)
    setattr(_args, 'test_data', test_doc_file)
    setattr(_args, 'fasttext_path', fasttext_path)
    setattr(_args, 'phase', phase)
    setattr(_args, 'db_filepath', db_path)
    out_file = test_set_file
    setattr(_args, 'out_file', out_file)
    return _args


def sentence_selection():
    phase = 'testing'
    _args = _construct_args_for_sentence_retrieval(phase)
    sentence_retrieval_ensemble_entrance(_args, calculate_fever_score=False)
    
    
if __name__=='__main__':
    
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, required=True, help='Add Path to Data Directory. See github for details on the data')
    parser.add_argument('--prefix', type=str, required=True, help='Add the data file prefix. Data: {prefix}.jsonl')
    
    args = parser.parse_args()

    data_dir = args.data_dir
    prefix = args.prefix
    
    # data_dir = '/fs/clip-scratch/navita/cmsc848Q'
    # prefix = 'presup'

    global db_path
    db_path = f'{data_dir}/data/fever/fever.db'
    
    doc_retrieval(data_dir, prefix)
    sent_retrieval(data_dir, prefix)
    sentence_selection()