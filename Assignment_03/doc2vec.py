import gensim
import pandas as pd
import io
import sys
from collections import namedtuple
import random
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
lot_review = pd.read_json('Tools_and_Home_Improvement_5.json', lines=True)
review_list = pd.read_json('reviews.json', lines=True)
all_text = list(review_list.text)+list(lot_review.reviewText)
docs = []
analyzedDocument = namedtuple('AnalyzedDocument', 'words tags')
for i, text in enumerate(all_text):
    words = text.lower().split()
    tags = [i]
    docs.append(analyzedDocument(words, tags))

model = gensim.models.Doc2Vec(docs, size=200, min_count=5, workers=8, window = 300)




'''model = gensim.models.Doc2Vec(size=300, window=10, min_count=5, workers=11,alpha=0.025, min_alpha=0.025)

model.build_vocab(docs)

for epoch in range(10):
    model.train(docs, total_examples=model.corpus_count,epochs=10)
    model.alpha -= 0.002            # decrease the learning rate
    model.min_alpha = model.alpha       # fix the learning rate, no deca
    model.train(docs)'''

model.save('doc2vec.w2v')

