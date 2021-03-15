import os
from nltk.stem import PorterStemmer
import string
import nltk


class SPIMI(object):
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.exclusion = list(string.punctuation) + list(string.digits)
        self.stop_words = list(nltk.corpus.stopwords.words('english'))
        self.posting_list = {}

    def directory_listing(self, root):
        files_in_dir = os.listdir(root)
        files_in_dir = [os.path.abspath(os.path.join(root, file)) for file in files_in_dir]
        return files_in_dir

    def file_reading(self, filename):
        with open(filename, 'r') as f:
            file_content = f.read()
        return file_content

    def tokenizer(self, file_content):
        tokens = [token for token in file_content.split() if token != '']
        return tokens

    def linguistic_transform(self, tokens):
        alphabet_only_tokens = []
        for token in tokens:
            new_token = ''
            for char in token:
                # Remove numerical and symbols
                if char not in self.exclusion:
                    new_token += char
            # Remove stopwords
            if new_token != '' and new_token not in self.stop_words:
                alphabet_only_tokens.append(new_token.lower())
        stem_tokens = [self.stemmer.stem(token) for token in alphabet_only_tokens]
        return stem_tokens

    def create_posting_list(self, token, doc_id):
        if token not in self.posting_list:
            self.posting_list[token] = {doc_id: 1}
        else:
            if doc_id not in self.posting_list[token]:
                self.posting_list[token][doc_id] = 1
            else:
                self.posting_list[token][doc_id] += 1

    def spimi_invert(self, root, block_size=500):
        files_in_dir = self.directory_listing(root)
        for idx, file in enumerate(files_in_dir):
            file_content = self.file_reading(file)
            tokens = self.linguistic_transform(self.tokenizer(file_content))
            for token in tokens:
                self.create_posting_list(token, idx)

            

if __name__ == '__main__':
    spimi = SPIMI()
    spimi.spimi_invert('HillaryEmails')
