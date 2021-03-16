import os
from nltk.stem import PorterStemmer
import string
import nltk
import sys
import time

# Run if first time
# nltk.download('stopwords')


class SPIMI(object):
    def __init__(self, output_dir):
        self.stemmer = PorterStemmer()
        self.exclusion = list(string.punctuation) + list(string.digits)
        self.stop_words = list(nltk.corpus.stopwords.words('english'))
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

    def directory_listing(self, root):
        files_in_dir = os.listdir(root)
        files_in_dir = [os.path.abspath(os.path.join(root, file)) for file in files_in_dir]
        return files_in_dir

    def file_reading(self, filename):
        with open(filename, 'r', encoding='utf8') as f:
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

    def add_to_dictionary(self, dictionary, term):
        dictionary[term] = []
        return dictionary[term]

    def get_postings_list(self, dictionary, term):
        return dictionary[term]

    def add_to_postings_list(self, postings_list, doc_id):
        postings_list.append(doc_id)

    def spimi_invert(self, root, block_size=100000):
        files_in_dir = self.directory_listing(root)
        block_num = 0
        # 1 block is 512 bytes (tracked by sys.getsizeof)
        max_byte = block_size * 512
        current_size = 0
        self.previous_dictionary = {}
        self.dictionary = {}
        self.start_time = time.time()
        for doc_id in (files_in_dir):
            file_content = self.file_reading(doc_id)
            tokens = self.linguistic_transform(self.tokenizer(file_content))
            for token in tokens:
                if token not in self.dictionary:
                    current_size += sys.getsizeof(token)
                    postings_list = self.add_to_dictionary(self.dictionary, token)
                else:
                    postings_list = self.get_postings_list(self.dictionary, token)
                if current_size + sys.getsizeof(doc_id) > max_byte:
                    self.write_block(self.dictionary, block_num)
                    self.block_time(block_num, current_size/512)
                    block_num += 1
                    self.dictionary = {}
                    current_size = 0
                    current_size += sys.getsizeof(token)
                    postings_list = self.add_to_dictionary(self.dictionary, token)
                    current_size += sys.getsizeof(doc_id)
                    self.add_to_postings_list(postings_list, doc_id)
                else:
                    current_size += sys.getsizeof(doc_id)
                    self.add_to_postings_list(postings_list, doc_id)
        if bool(self.dictionary):
            self.write_block(self.dictionary, block_num)
            self.block_time(block_num, current_size/512)

    def block_time(self, block_num, block_size):
        end_time = time.time()
        print(f'Time take for BLOCK {block_num}: {end_time-self.start_time}, BLOCK {block_num} size: {block_size}')
        self.start_time = time.time()

    def write_block(self, dictionary, block_num):
        sorted_terms = [term for term in sorted(dictionary)]
        output_block_file = os.path.join(self.output_dir, f'BLOCK{block_num}.txt')
        with open(output_block_file, 'w', encoding='utf8') as f:
            for term in sorted_terms:
                line = f'{term} {" ".join([str(doc_id) for doc_id in dictionary[term]])}'
                f.write(line)
        return output_block_file
            

if __name__ == '__main__':
    spimi = SPIMI('output/')
    spimi.spimi_invert('HillaryEmails')
