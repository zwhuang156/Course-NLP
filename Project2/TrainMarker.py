import csv
import jieba
import operator

SizeOfMarker = 50

class word():
	def __init__(self):
		self.relation = {}
		self.relation['Contingency'] = 0
		self.relation['Expansion'] = 0
		self.relation['Temporal'] = 0
		self.relation['Comparison'] = 0
		
		self.been_judged = 0
		self.marker = 0
		self.result = 'Unknown'
		
class Trainer():
	def __init__(self):
		self.data_folder = "./data/train.csv"
		self.test_data = "./data/test.csv"
		
		# jieba custom setting.
		jieba.set_dictionary('jieba_dict/dict.txt.big')
		
		# load stopwords set
		self.stopwordset = set()
		with open('jieba_dict/stop_words.txt','r',encoding='utf-8') as sw:
			for line in sw:
				self.stopwordset.add(line.strip('\n'))
		# D[word] = word()
		self.D = {}
		
	def parse_train(self):
		with open(self.data_folder) as file:
			count = 0
			for line in file:
				if count!=0:
					line = line.strip().split(',')
					if line[3]!='1':
						sentence_1 = self.segment(line[1])
						sentence_2 = self.segment(line[2])
						for seg in sentence_1:
							try:
								self.D[seg].relation[line[3]] += 1				
							except:
								self.D[seg] = word()
								self.D[seg].relation[line[3]] += 1
						for seg in sentence_2:
							try:
								self.D[seg].relation[line[3]] += 1				
							except:
								self.D[seg] = word()
								self.D[seg].relation[line[3]] += 1
				else: count+=1
		
	def segment(self, line):
		result = []
		words = jieba.cut(line, cut_all=False)
		for seg in words:
			if seg not in self.stopwordset:
				result.append(seg)
		return result
		
	def ParseTestAndOutput(self):
		submission = open('submit.csv', 'w')
		submission.write('Id,Relation\n')
		count = 0
		marker_exp = self.judge_marker_V2('Expansion')
		marker_con = self.judge_marker_V2('Contingency')
		marker_tem = self.judge_marker_V2('Temporal')
		marker_com = self.judge_marker_V2('Comparison')
		
		marker_exp['不只'] = 100
		marker_exp['還是'] = 100
		marker_exp['例如'] = 100
		marker_exp['或是'] = 100
		marker_con['假如'] = 100
		marker_tem['同時'] = 100
		marker_tem['後來'] = 100
		marker_tem['正當'] = 100
		marker_tem['現在'] = 100
		marker_tem['之前'] = 100
		marker_com['可是'] = 100
		marker_com['即使'] = 100
		marker_com['然而'] = 100
		
		
		print(marker_exp)
		print(marker_con)
		print(marker_tem)
		print(marker_com)
		
		with open(self.test_data) as file:
			for line in file:
				line_dict = {'Contingency':0, 'Expansion':0, 'Temporal':0, 'Comparison':0}
				if count!=0:
					line = line.strip().split(',')
					sentence_1 = self.segment(line[1])
					sentence_2 = self.segment(line[2])
					sentence = sentence_1 + sentence_2
					for seg in sentence:
						if seg in marker_exp:
							line_dict['Expansion'] += 1
						if seg in marker_con:
							line_dict['Contingency'] += 1
						if seg in marker_tem:
							line_dict['Temporal'] += 1
						if seg in marker_com:
							line_dict['Comparison'] += 1				
					result_val = max(line_dict.items(), key=operator.itemgetter(1))[1]
					if result_val > 0:
						result = max(line_dict.items(), key=operator.itemgetter(1))[0]
					else:
						result = 'Expansion'
					submission.write('%s,%s\n' %(line[0], result))
				else: count+=1

	def judge_marker_V2(self , relation_type):
		marker = {}
		for key in self.D:
			if len(marker) < SizeOfMarker:
				marker[key] = self.D[key].relation[relation_type]
			elif len(marker)==SizeOfMarker:
				min_key = min(marker.items(), key=operator.itemgetter(1))[0]
				min_val = min(marker.items(), key=operator.itemgetter(1))[1]
				if self.D[key].relation[relation_type] > min_val:
					marker.pop(min_key,None)
					marker[key] = self.D[key].relation[relation_type]
		return marker
				
if __name__ == '__main__':
	trainer = Trainer()
	trainer.parse_train()
	trainer.ParseTestAndOutput()
	
	
			
			
			
			
		
		
		
		
