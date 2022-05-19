### FEVER

- Document Retreival (ATHENE): [doc_ret](/fever/doc_ret)  
- Sentence Selection + NLI (KGAT): [kgat](/fever/kgat)


### Setup Instruction

```
conda create fever python=3.6
conda activate fever
pip install -r requirements.txt
```

### Data and Model Requirements

```
export data_dir = /path/to/data/
```

- Step 1: Download Wikipedia data
```
wget https://s3-eu-west-1.amazonaws.com/fever.public/wiki-pages.zip
unzip wiki-pages.zip -d $data_dir
```

- Step 2: Create FEVER database
```
cd doc_ret
PYTHONPATH=src python src/scripts/build_db.py $data_dir/wiki-pages $data_dir/fever/fever.db
```
The script for creating database is in [doc_ret](doc_ret) folder

- Step 3: Download pre-trained FastText Vectors
```
wget https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki.en.zip
mkdir $data_dir/fasttext
unzip wiki.en.zip -d $data_dir/fasttext
```

- Step 4: Download KGAT data and checkpoints
```
wget https://thunlp.oss-cn-qingdao.aliyuncs.com/KernelGAT/FEVER/KernelGAT.zip
unzip KernelGAT.zip -d kgat
```

- Step 5: Clean up all zip files
```
rm *.zip
```


