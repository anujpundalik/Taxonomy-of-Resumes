import InfoExtract
from gensim.models import Word2Vec

finalVector = InfoExtract.getFinalVector()

global model

model = Word2Vec(finalVector, size=200, window=10, min_count=3, workers=4)

model.save("TestModel")
print(list(model.wv.vocab))