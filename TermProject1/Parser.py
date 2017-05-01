import pandas as pd
import csv


class Parser():
    """docstring for Parser"""
    def __init__(self):
        self.data_folder = "./data/"
        self.filter_punc = ",，.．。!！?？-()（）「」『 』:：、; "

    '''
    if parse aspect_term.txt the size = 4
    else parse test.review.txt the size = 2
    '''
    def parse_review(self, file_name, size):
        index = 0
        aspect_review_list = []
        with open(self.data_folder + file_name) as file:
            aspect = []
            for line in file:
                # print line.strip()
                line = line.strip()
                for punc in self.filter_punc:
                    line = line.replace(punc, ',')
                aspect.append(line)
                index += 1
                if index == size:
                    index = 0
                    aspect_review_list.append(aspect)
                    aspect = []
        return aspect_review_list

    def test_review(self):
        index = 0
        review_id = 0
        aspect_review_list = {}
        with open(self.data_folder + 'test_review.txt') as file:
            for line in file:
                line = line.strip()
                if index == 0:
                    review_id = line
                    index +=1
                elif index == 1:
                    for punc in self.filter_punc:
                        line = line.replace(punc, ',')
                    aspect_review_list[review_id] = line
                    index = 0
        return aspect_review_list

    def read_test(self):
        csv_reader = list(csv.reader(open(self.data_folder + 'test.csv')))
        return csv_reader[1:]

    def read_aspect_term(self):
        with open(self.data_folder + 'aspect_term.txt') as file:
            aspect_term = {}
            for line in file:
                line = line.strip('\n').split('\t')
                aspect = line[0]
                terms = line[1].split(' ')
                terms.append(aspect)
                aspect_term[aspect] = terms
        return aspect_term



    def negative(self):
        with open(self.data_folder + 'NTUSD_neg.txt') as file:
            negative_word = []
            for line in file:
                line = line.strip('\n')
                negative_word.append(line)
        return negative_word

    def positive(self):
        with open(self.data_folder + 'NTUSD_pos.txt') as file:
            negative_word = []
            for line in file:
                line = line.strip('\n')
                negative_word.append(line)
        return negative_word


if __name__ == '__main__':
    parser = Parser()
    parser.parse_review('aspect_review_half.txt', 4)
    print (parser.read_aspect_term())
