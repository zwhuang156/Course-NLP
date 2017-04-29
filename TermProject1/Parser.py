class Parser():
    """docstring for Parser"""
    def __init__(self):
        self.data_folder = "./data/"

    def aspect_review(self):
        index_size = 4
        index = 0
        aspect_review_list = []
        with open(self.data_folder + 'aspect_review_half.txt') as file:
            each_aspect = []
            for line in file:
                # print line.strip()
                each_aspect.append(line.strip().decode('utf-8'))
                index += 1
                if index == 4:
                    index = 0
                    aspect_review_list.append(each_aspect)
                    each_aspect = []
        return aspect_review_list

if __name__ == '__main__':
    parser = Parser()
    aspect_review_list = parser.aspect_review()
    print aspect_review_list
