from Parser import Parser
import nltk
from nltk.collocations import *
import jieba

parser = Parser()
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()
filter_list = '~!@#$%^&*()_+`1234567890-=\\{\\}[]\|;:\'\"><:;,.?/'

def main():
    aspect_review_list = parser.aspect_review()
    for line in aspect_review_list:
        print line[0]
        print '/'.join(jieba.cut(line[1]))
        # finder = BigramCollocationFinder.from_words(jieba.cut(line[1]))
        # finder.apply_word_filter(lambda w: w.lower() in filter_list)
        # for a, b in finder.nbest(bigram_measures.pmi, 10):
        #     print "%s, %s" %(a, b)

        # print "======="

        # finder = TrigramCollocationFinder.from_words(jieba.cut(line[1]))
        # finder.apply_word_filter(lambda w: w.lower() in filter_list)
        # for a, b, c in finder.nbest(trigram_measures.pmi, 10):
        #     print "%s, %s, %s" %(a, b, c)
if __name__ == '__main__':
    main()
