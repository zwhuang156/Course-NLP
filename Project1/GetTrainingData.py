import jieba
import logging

class parse_polarity():
	
	def __init__(self):
		logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
		
		self.data_folder = "./data/"
		self.filter_punc = ",，.．。!！?？-()（）「」『 』:：、;；～~ "
		
		# jieba custom setting.
		jieba.set_dictionary('jieba_dict/dict.txt.big')

		# load stopwords set
		self.stopwordset = set()
		with open('jieba_dict/stop_words.txt','r',encoding='utf-8') as sw:
			for line in sw:
				self.stopwordset.add(line.strip('\n'))
	
	def polarity_review(self,file_name):
		texts_num = 0
		output = open('train_data.txt','w')
		
		with open(self.data_folder + file_name) as file:
			for line in file:
				line = line.lstrip('-1')
				line = line.lstrip()
				words = jieba.cut(line, cut_all=False)
				for word in words:
					if not (word in self.stopwordset or word in self.filter_punc):
						output.write(word +' ')
				texts_num += 1
				if texts_num % 10000 == 0:
					logging.info("已完成前 %d 行的斷詞" % texts_num)
		output.close()
	
	
	
if __name__ == '__main__':
	parser = parse_polarity()
	parser.polarity_review('polarity_review.txt')
	

