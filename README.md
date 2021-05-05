# SPIMI
Single-pass in-memory indexing

## Getting Started
### Requirements
We make use of the nltk library for stemming and porting
```
$ pip install nltk
```

While running this for the first time, ensure to uncomment 
```
nltk.download('stopwords')
```
### Running the search engine
First we need the inverted index
```
$ python spimi.py --path <input folder> --block_size <user preferred block size> --output <output directory> --filename <output index filename>
```

After creating the inverted index, we will be able to run searches with
```
$ python search.py --search <words to search> --index <path to index file> --mode <AND or OR> --ranked (optional to enable ranked search)
```