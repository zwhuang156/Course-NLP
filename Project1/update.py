from gensim.models import word2vec
from gensim import models
import jieba


def update_aspect():

	model = models.Word2Vec.load('med250.model.bin')
	
	output = open("./data/new_aspect_term.txt","w")
	
	with open("./data/aspect_term.txt") as file:
		for line in file:
			line = line.strip()
			words = line.split()
			for word in words:
				res = model.most_similar(word,topn = 300)
				for item in res:
					if item[1]>0.6:
						line = line + ' ' + item[0]
			line = line + '\n'
			output.write(line)
		
def update_PosNeg(file_name):
	model = models.Word2Vec.load('med250.model.bin')
	
	output_pos = open("./data/new_"+file_name,"w")
	
	with open("./data/"+file_name) as file:
		for line in file:
			word = line.strip()
			try:
				res = model.most_similar(word,topn = 200)
				output_pos.write('\n'+word)
				for item in res:
					if item[1]>0.65:
						output_pos.write('\n'+item[0])
			except:
				pass

	
			
if __name__ == '__main__':
	update_aspect()
	#update_PosNeg("NTUSD_pos.txt")
	#update_PosNeg("NTUSD_neg.txt")