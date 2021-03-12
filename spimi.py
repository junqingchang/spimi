import os
from nltk.stem import PorterStemmer


class SPIMI(object):
    def __init__(self):
        self.stemmer = PorterStemmer()

    def spimi_invert(self):
        pass

    def directory_listing(self, root):
        files_in_dir = os.listdir(root)
        files_in_dir = [os.path.abspath(os.path.join(root, x)) for x in files_in_dir]
        return files_in_dir

    def file_reading(self, filename):
        with open(filename, 'r') as f:
            file_contents = f.read()
        return file_contents

    def tokenizer(self):
        pass

    def linguistic_transform(self):
        pass


if __name__ == '__main__':
    spimi = SPIMI()
    files = spimi.directory_listing('HillaryEmails')
    print(files[0])
    print(spimi.file_reading(files[0]))