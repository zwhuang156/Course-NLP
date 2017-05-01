class Parser():
    """docstring for Parser"""
    def __init__(self):
        self.data_folder = "./data/"
        self.filter_punc = ",，.．。!！?？-()「」『 』:、; "

    def aspect_review(self):
        index_size = 4
        index = 0
        aspect_review_list = []
        with open(self.data_folder + 'aspect_review_half.txt') as file:
            each_aspect = []
            for line in file:
                # print line.strip()
                line = line.strip()
                for punc in self.filter_punc:
                    line = line.replace(punc, '')
                each_aspect.append(line)
                index += 1
                if index == 4:
                    index = 0
                    aspect_review_list.append(each_aspect)
                    each_aspect = []
        return aspect_review_list

if __name__ == '__main__':
    parser = Parser()
    aspect_review_list = parser.aspect_review()
    for line in aspect_review_list:
        print (line[1])
