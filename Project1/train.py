from gensim.models import word2vec
import logging


def data_training():
	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	sentences = word2vec.Text8Corpus("train_data.txt")
	model = word2vec.Word2Vec(sentences, size=250)

	# Save our model.
	model.save("pol.model.bin")

	# To load a model.
	# model = word2vec.Word2Vec.load("your_model.bin")

if __name__=="__main__":
	data_training()