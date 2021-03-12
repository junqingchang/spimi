import os
from nltk.stem import PorterStemmer
import string


class SPIMI(object):
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.exclusion = list(string.punctuation) + list(string.digits)

    def spimi_invert(self):
        pass

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
                if char not in self.exclusion:
                    new_token += char
            if new_token != '':
                alphabet_only_tokens.append(new_token.lower())
        stem_tokens = [self.stemmer.stem(token) for token in alphabet_only_tokens]
        return stem_tokens


if __name__ == '__main__':
    spimi = SPIMI()
    files = spimi.directory_listing('HillaryEmails')
    file_content = spimi.file_reading(files[0])
    tokens = spimi.tokenizer(file_content)
    stemed = spimi.linguistic_transform(tokens)