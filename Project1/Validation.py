from Parser import Parser
import random

data_folder = "./data"
validation_review_name = data_folder + "/validation_review.txt"
validation_name = data_folder + '/validation.csv'
answer_name = data_folder + '/answer.csv'
submit_name = './submit.csv'

parser = Parser()
whole_aspect = ["服務", "環境", "價格", "交通", "餐廳"]

def evaluate():
    answer_list = []
    submit_list = []
    answer_file = open(answer_name, 'r')
    submit_file = open(submit_name, 'r')
    for index, line in enumerate(answer_file):
        line = line.strip()
        line = line.split(',')
        if index == 0:
            continue
        answer_list.append(line[1])

    for index, line in enumerate(submit_file):
        line = line.strip()
        line = line.split(',')
        if index == 0:
            continue
        submit_list.append(line[1])
    
    correct = 0
    for index, answer_label in enumerate(answer_list):
        submit_label = submit_list[index]
        if submit_label == answer_label:
            correct += 1

    print ("Accuracy rate: %f" %(correct / len(answer_list)))


def validation():
    validation_review_file =  open(validation_review_name, 'w')
    validation_file = open(validation_name, 'w')
    validation_file.write('Id,Review_id,Aspect\n')
    answer_file = open(answer_name, 'w')
    answer_file.write("Id,Label\n")
    aspect_review_list = parser.parse_review('aspect_review.txt', 4)
    validation_id = 1
    for line in aspect_review_list:
        review_id = line[0]
        content = line[1]
        pos_aspect = line[2]
        neg_aspect = line[3]
        content_aspect = []
        for aspect in pos_aspect:
            if aspect != '':
                validation_file.write('%s,%s,%s\n' %(validation_id, review_id, aspect))
                answer_file.write('%s,%s\n' %(validation_id, '1'))
                validation_id += 1
                content_aspect.append(aspect)
        for aspect in neg_aspect:
            if aspect != '':
                validation_file.write('%s,%s,%s\n' %(validation_id, review_id, aspect))
                answer_file.write('%s,%s\n' %(validation_id, '-1'))
                validation_id += 1
                content_aspect.append(aspect)
        if len(content_aspect) < 3:   
            for aspect in whole_aspect:
                if aspect not in content_aspect:
                    if random.random() > 0.5:
                        validation_file.write('%s,%s,%s\n' %(validation_id, review_id, aspect))
                        answer_file.write('%s,%s\n' %(validation_id, '0'))
                        validation_id += 1

        validation_review_file.write(review_id + '\n')
        validation_review_file.write(content + '\n')
    validation_review_file.close()
    validation_file.close()
    answer_file.close()

if __name__ == '__main__':
    validation()
    evaluate()