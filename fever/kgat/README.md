## FEVER: Sentence Selection and NLI (KGAT)

### Sentence Selection
#### Input
- Description: Candidate sentences from Document Retrieval  
- Location: {data_dir}/output/docs/{prefix}.sent.7.jsonl  
- Example 

> {"id": 0, "claim": "", "evidence":[[page_title_1, sent_num, evidence_string], [page_title_1, sent_num, evidence_string], ...]

The evidence set contains the a 3 element array for each evidence sentence of the form [page_title, sent_num, evidence_string]

- page_title: Title of wikipedia page
- sent_num: The position of sentence in the respective wikipedia page
- evidence_string: Evidence text


#### Run Instructions

```
export prefix='tmp'
cd kgat/retrieval_model

python test.py --outdir ./output/ --test_path /fs/clip-scratch/navita/cmsc848Q/output/docs/$prefix.sent.7.jsonl --bert_pretrain ../bert_base --checkpoint ../checkpoint/retrieval_model/model.best.pt --name $prefix.json

python process_data.py --retrieval_file ./output/$prefix.json --gold_file /fs/clip-scratch/navita/cmsc848Q/output/docs/$prefix.sent.7.jsonl  --output ./output/bert_$prefix.json --test

```

#### Output
Sentence selection returns 5 evidence per claim

[test.py](/fever/kgat/retrieval_model/test.py)
- Location: ./output/{prefix}.json file  
- Example
> {id: 0, evidence: [[page_title, sent_num, evidence_string, 0, evidence_score], [page_num, sent_num, evidence_string, 0, evidence_score], ..]}

- The evidence set contains list of 5 evidence per claim   
- evidence_score: Weight of the respective evidence piece (between -1 to  1)

> **_NOTE:_** The 0 in the evidence set is spurious

[process_data.py](/fever/kgat/retrieval_model/process_data.py) 
- Location: ./output/bert_{prefix}.json file  
- Example 

> {id: 0, claim: "", evidence:[[page_title, sent_num, evidence_string, 0, evidence_score], ...]}




### NLI
#### Input
- The output of [process_data.py](/fever/kgat/retrieval_model/process_data.py) as described above

#### Run Instructions

```
export prefix='tmp'
cd kgat/kgat

python test.py --outdir ./output/ --test_path ../retrieval_model/output/bert_$prefix.json --bert_pretrain ../bert_base --checkpoint ../checkpoint/kgat/model.best.pt --name $prefix.json
```

#### Output 
- Location: ./output/{prefix}.json  
- Example

> {id: 0, predicted_label: "SUPPORTS"}

Predicted label: The NLI label ["SUPPORTS", "REFUTES", "NOT ENOUGH INFO"]

