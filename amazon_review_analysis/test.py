import json
import pandas as pd
import spacy
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from imblearn.over_sampling import RandomOverSampler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.svm import SVC
svc = SVC()
nlp = spacy.load('en')
review_list = pd.read_json('reviews.json', lines=True)
class PartOfSpeechFilter(BaseEstimator, TransformerMixin):
    def __init__(self, pos_to_keep=('NOUN', 'PROPN', 'ADJ', 'VERB'), stop_words=None):
        self.pos_to_keep = pos_to_keep
        self.stop_words = stop_words

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        preprocessed_sentences = []

        for doc in nlp.pipe(X, n_threads=8):
            if self.stop_words is not None:
                keep_tokens_string = ' '.join([t.lemma_ for t in doc if t.pos_ in self.pos_to_keep and t.lemma_ not in self.stop_words])
            else:
                keep_tokens_string = ' '.join([t.lemma_ for t in doc if t.pos_ in self.pos_to_keep])
        preprocessed_sentences.append(keep_tokens_string)

        return preprocessed_sentences




cv = CountVectorizer(lowercase=True, stop_words='english',)
posf = PartOfSpeechFilter()
y = review_list.score.values
pipeline = Pipeline([('posf', PartOfSpeechFilter()),
                     ('cv', CountVectorizer(lowercase=True))
                     ])

pipeline.set_params(**{'posf__stop_words': {'flashlight','-PRON-'}})
pipeline.set_params(cv__max_df=0.95, cv__min_df=0.01)

preproc_reviews_withstop = pipeline.fit_transform(review_list.text)

c_range = np.linspace(100, 200, 5 )

rus = RandomOverSampler()
X_resampled, y_resampled = rus.fit_sample(preproc_reviews_withstop, y)
def main():
    param_svc= dict(kernel = ['linear','poly', 'rbf', 'sigmoid'], C = c_range)#find the best kernel ,C = c_range
    grid_search_solver = GridSearchCV(svc, param_grid=param_svc, n_jobs=-1,cv =5,scoring= 'accuracy')
    grid_search_solver.fit(X_resampled, y_resampled)
    print(grid_search_solver.best_params_)

if __name__ == '__main__':
    main()
