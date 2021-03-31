import argparse


class Searcher(object):
    def __init__(self, index_file, query):
        self.index_file = index_file
        self.query = query
        self.query_files = []
        with open(self.index_file, 'r', encoding='utf-8') as f:
            for line in f:
                line_split = line.split()
                term = line_split[0]
                related_files = line_split[1:]
                if term in self.query:
                    self.query_files.append(related_files[:])

    def run_query(self, mode='AND', exclude=None):
        if mode == 'AND':
            output = self.and_query(exclude)
        elif mode == 'OR':
            output = self.or_query(exclude)

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


parser = argparse.ArgumentParser(description='Single-Pass In-Memory Indexing')
parser.add_argument('--index', default='output/index.txt')
parser.add_argument('--search', nargs='+', required=True)
parser.add_argument('--mode', default='AND')
parser.add_argument('--exclude', default=None)
args = parser.parse_args()


if __name__ == '__main__':
    searcher = Searcher(args.index, args.search)
    searcher.run_query(args.mode, exclude=args.exclude)