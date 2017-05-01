from Parser import Parser
import nltk
from nltk.collocations import *
from gensim.models import word2vec
import jieba

parser = Parser()
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()
filter_list = '~!@#$%^&*()_+`-=\\{\\}[]\|;:\'\"><:;,.?/'

def transform_y(pos_opinion, neg_opinion):
    y = [0.5]*5
    for category in pos_opinion:
        if category == "服務":
            y[0] = 1.0
        if category == "環境":
            y[1] = 1.0
        if category == "價格":
            y[2] = 1.0
        if category == "交通":
            y[3] = 1.0
        if category == "餐廳":
            y[4] = 1.0

    for category in neg_opinion:
        if category == "服務":
            y[0] = 0.0
        if category == "環境":
            y[1] = 0.0
        if category == "價格":
            y[2] = 0.0
        if category == "交通":
            y[3] = 0.0
        if category == "餐廳":
            y[4] = 0.0
    return y


def review_to_vec(w2v):
    x_train = []
    y_train = []
    for line in parser.aspect_review():
        review = ' '.join(jieba.cut(line[1]))
        if len(line[2]) != 0:
            pos_opinion = line[2].split('\t')
        if len(line[3]) != 0:
            neg_opinion = line[3].split('\t')
        y_train.append(transform_y(pos_opinion, neg_opinion))
        sequnence = []
        for character in review:
            sequnence.append(model.wv[character])
        x_train.append(sequnence)
    return x_train, y_train

def main():

    x_train, y_train = review_to_vec(word2vec.Word2Vec.load("med250.model.bin"))
    print('x_train shape:', x_train.shape)
    print('y_train shape:', y_train.shape)


    # aspect_review_list = parser.aspect_review()
    # for line in aspect_review_list:
    #     print (line[0])
    #     print (' '.join(jieba.cut(line[1])))
    #     print (len(line[2]))
    #     # finder = BigramCollocationFinder.from_words(jieba.cut(line[1]))
    #     # finder.apply_word_filter(lambda w: w.lower() in filter_list)
    #     # for a, b in finder.nbest(bigram_measures.pmi, 10):
    #     #     print "%s, %s" %(a, b)

    #     # print "======="

    #     # finder = TrigramCollocationFinder.from_words(jieba.cut(line[1]))
    #     # finder.apply_word_filter(lambda w: w.lower() in filter_list)
    #     # for a, b, c in finder.nbest(trigram_measures.pmi, 10):
    #     #     print "%s, %s, %s" %(a, b, c)
if __name__ == '__main__':
    main()
