## Document Retrieval

### Input

- Location: {data_dir}/data/fever/{prefix}.jsonl  
- Example

> {"id": 0, "claim": "there is some reason that european countries gave up their colonies in southeast asia"}


### Run Instructions
```
python main.py --data_dir={data_dir} --prefix={prefix}
```

> data_dir: base_dir containing data/db/output folders. 

See [../fever](/fever/) for instructions   
> prefix: name of the jsonl file without file extension.

### Output
Extracted wiki documents and sentences   
- wiki_documents: {data_dir}/output/docs/{prefix}.wiki.7.jsonl   
- sentences: {data_dir}/output/docs/{prefix}.sent.7.jsonl

