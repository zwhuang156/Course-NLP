from Parser import Parser
import jieba

class ReviewOpinion(object):
    """docstring for ReviewOpinion"""
    def __init__(self):
        self.parser = Parser()
        # jieba custom setting.
        jieba.set_dictionary('jieba_dict/dict.txt.big')

        # load stopwords set
        self.stopwordset = set()
        with open('jieba_dict/stopwords.txt','r',encoding='utf-8') as sw:
            for line in sw:
                self.stopwordset.add(line.strip('\n'))

    def segment(self, line):
        result = []
        words = jieba.cut(line, cut_all=False)
        for word in words:
            if word not in self.stopwordset:
                result.append(word)
        return result

    def main(self):
        file = open('submit.csv', 'w')
        file.write('Id,Label\n')
        test_review = self.parser.test_review()
        test_csv = self.parser.read_test()
        neg_words = self.parser.negative()
        pos_words = self.parser.positive()
        aspect_term = self.parser.read_aspect_term()
        for line in test_csv:
            review_id = line[1]
            target_aspect = line[2]
            content = test_review[review_id].split(',')

            score = 0
            terms = aspect_term[target_aspect]
            for sentence in content:
                for term in terms:
                    if term in sentence:
                        sentence_segment = self.segment(sentence)
                        for character in sentence_segment:
                            if character in neg_words:
                                score -= 1
                            elif character in pos_words:
                                score += 1
            opinion = 0
            if score > 0:
                opinion = 1
            elif score < 0:
                opinion = -1
            file.write('%s,%d\n' %(line[0], opinion))

if __name__ == '__main__':
    reviewOpinion = ReviewOpinion()
    reviewOpinion.main()