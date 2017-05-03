from Parser import Parser
import jieba.posseg as pseg
import jieba

parser = Parser()
# print (parser.polarity_review())
for line in parser.polarity_review():
	opinion = line[0]
	content = line[1]
	segments = pseg.cut(content)
	for word, flag in segments:
		print ('%s, %s' %(word, flag))