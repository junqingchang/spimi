import argparse
import nltk
import string
from nltk.stem import PorterStemmer
import os
import math


all_docs_directory = 'HillaryEmails/'


class Searcher(object):
    def __init__(self, index_file, query, ranked=False):
        self.index_file = index_file
        self.query = query
        self.ranked = ranked
        self.query_files = []
        if not self.ranked:
            with open(self.index_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line_split = line.split()
                    term = line_split[0]
                    related_files = line_split[1:]
                    if term in self.query:
                        self.query_files.append(related_files[:])
        else:
            self.df_files = []
            for i in range(len(self.query)):
                self.df_files.append([])
            with open(self.index_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line_split = line.split()
                    term = line_split[0]
                    related_files = line_split[1:]
                    if term in self.query:
                        self.df_files[self.query.index(term)] += (related_files[:])
                        self.query_files.append(related_files[:])

    def run_query(self, mode='AND', exclude=None):
        if mode == 'AND':
            if not self.ranked:
                output = self.and_query(exclude)
            else:
                output = self.tfidf_and_query()
        elif mode == 'OR':
            if not self.ranked:
                output = self.or_query(exclude)
            else:
                output = self.tfidf_or_query()

        if len(output) != 0:
            print(f'The following documents contains: {f" {mode} ".join(self.query)}')
            for document in output:
                print(document)
        else:
            print(f'No documents found that contains: {f" {mode} ".join(self.query)}')

        return output

    def and_query(self, exclude):
        if self.query_files == []:
            return []
        output = set(self.query_files[0])
        for i in range(1, len(self.query_files)):
            output = output.intersection(self.query_files[i])
        return output

    def or_query(self, exclude):
        if self.query_files == []:
            return []
        output = set(self.query_files[0])
        for i in range(1, len(self.query_files)):
            output = output.union(self.query_files[i])
        return output

    def linguistic_transform(self, tokens):
        stemmer = PorterStemmer()
        inclusion = list(string.ascii_lowercase) + list(string.ascii_uppercase)
        stop_words = list(nltk.corpus.stopwords.words('english'))
        alphabet_only_tokens = []
        for token in tokens:
            new_token = ''
            for char in token:
                # Remove numerical and symbols
                if char in inclusion:
                    new_token += char
            # Remove stopwords
            if new_token != '' and new_token not in stop_words:
                alphabet_only_tokens.append(new_token)
        stem_tokens = [stemmer.stem(token).lower() for token in alphabet_only_tokens]
        return stem_tokens

    def tokenizer(self, file_content):
        tokens = [token for token in file_content.split() if token != '']
        return tokens

    def tfidf_and_query(self):
        if self.query_files == []:
            return []

        output = set(self.query_files[0])
        for i in range(1, len(self.query_files)):
            output = output.intersection(self.query_files[i])
        output = list(output)
        if len(output) == 0:
            return []

        tfs = []
        dfs = []
        dfs = [len(set(qf)) for qf in self.df_files]
        N = len(os.listdir(all_docs_directory))

        for i in range(len(output)):
            tfs.append([])
            for j in range(len(self.query)):
                tfs[i].append(0)
        for i in range(len(self.df_files)):
            for j in range(len(self.df_files[i])):
                if self.df_files[i][j] in output:
                    tfs[output.index(self.df_files[i][j])][i] += 1

        tfidf = []
        for i in range(len(tfs)):
            curr_tfidf = 0
            tf = tfs[i]
            for j in range(len(tf)):
                curr_tfidf += math.log(1+tf[j]) * math.log(N/dfs[j])
            tfidf.append(curr_tfidf)
        dupp = []
        final_output = []
        for value in sorted(tfidf, reverse=True):
            if value not in dupp:
                final_output += [output[i] for i, curr in enumerate(tfidf) if curr == value]
                dupp.append(value)
        return final_output
        
    def tfidf_or_query(self):
        if self.query_files == []:
            return []

        output = set(self.query_files[0])
        for i in range(1, len(self.query_files)):
            output = output.union(self.query_files[i])
        output = list(output)
        if len(output) == 0:
            return []

        tfs = []
        dfs = [len(set(qf)) for qf in self.df_files]
        N = len(os.listdir(all_docs_directory))

        for i in range(len(output)):
            tfs.append([])
            for j in range(len(self.query)):
                tfs[i].append(0)
        for i in range(len(self.df_files)):
            for j in range(len(self.df_files[i])):
                if self.df_files[i][j] in output:
                    tfs[output.index(self.df_files[i][j])][i] += 1

        tfidf = []
        for i in range(len(tfs)):
            curr_tfidf = 0
            tf = tfs[i]
            for j in range(len(tf)):
                curr_tfidf += math.log(1+tf[j]) * math.log(N/dfs[j])
            tfidf.append(curr_tfidf)
        dupp = []
        final_output = []
        for value in sorted(tfidf, reverse=True):
            if value not in dupp:
                final_output += [output[i] for i, curr in enumerate(tfidf) if curr == value]
                dupp.append(value)
        return final_output


parser = argparse.ArgumentParser(description='Single-Pass In-Memory Indexing')
parser.add_argument('--index', default='output/index.txt')
parser.add_argument('--search', nargs='+', required=True)
parser.add_argument('--mode', default='AND')
parser.add_argument('--exclude', default=None)
parser.add_argument('--ranked', default=False, action='store_true')
args = parser.parse_args()


if __name__ == '__main__':
    searcher = Searcher(args.index, args.search, args.ranked)
    searcher.run_query(args.mode, exclude=args.exclude)

## Use shirer selv for experiment