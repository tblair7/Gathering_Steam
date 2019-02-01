import pandas as pd
import numpy as np

from sklearn.base import TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import WhitespaceTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.lancaster import LancasterStemmer


ws_tokenizer = WhitespaceTokenizer()
lancaster = LancasterStemmer()
porter = PorterStemmer()
snowball = SnowballStemmer('english')

try:
    stopwords = set(stopwords.words('english'))
except:
    nltk.download('stopwords')
    stopwords = set(stopwords.words('english'))


stop_list = ['like', 'game', 'ark', 'played', 'play', 'love', 'good', 'pretty', 'game',
            'fun', 'great', 'lot', 'best', 'awesome', 'ok', 'better', 'probably', 'games',]



######


def cleanText(text):

    # import a dictionary of English contractions from another file
    from contractions import contractions_dict
    contraction_dict = contractions_dict

    # replace the contractions with their expanded form
    for contraction, expansion in contraction_dict.items():
        text = text.replace(contraction.lower(),expansion.lower())

    # get rid of newlines
    symbols = ['\'', '\"', '.', ',', '[', ']', '(', ')', '?', '!', '@', '$', '#', '&', '%']

    text = text.strip().replace('\n', ' ').replace('\r', ' ').replace('-',' ')



    for symbol in symbols:
        text = text.replace(symbol, '')

    # lowercase
    text = text.lower()

    return text



######



def gen_tokens(review, *args):

    ws_tokenized = ws_tokenizer.tokenize(review)

    cleaned_tokens = []

    for token in ws_tokenized:
        if token not in stopwords:
            cleaned_tokens.append(token.lower().strip())


    clean_tokens =  ' '.join(cleaned_tokens)

    return clean_tokens



######



def clean_and_tokenize(reviews):

    cleaned_reviews = []

    for review in reviews:
        review_tokens = []
        cleaned_text = cleanText(review)
        cleaned_reviews.append(gen_tokens(cleaned_text))

    return cleaned_reviews



######


def display_topics(vectorizer, clf, W, df, num_top_words, num_top_reviews):
    ''' Print out topics discovered by a model '''

    # get list of feature names
    feature_names = vectorizer.get_feature_names()

    # get vader sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # list of topics and reviews to return
    topics = []

    # loop over all the topics
    for topic_id, topic in enumerate(clf.components_):

        sentiment_sum = 0

        # grab the list of words describing the topic
        word_list = []
        for i in topic.argsort()[:-num_top_words - 1:-1]:
            word_list.append(feature_names[i])

        # split words in case there are some bigrams and get unique set
        split_list = []
        for word in word_list:
            for split in word.split():
                split_list.append(split)

        topic_words = list(set(split_list))

        # append topic words as a single string
        topics.append(' '.join([word for word in topic_words]))

    return topics



def topics(df, params, index_dictionary):


    num_features = params['num_features']
    num_topics = params['num_topics']
    num_top_words = params['num_top_words']
    num_top_reviews = params['num_top_reviews']

    vectorizer = TfidfVectorizer(stop_words=stop_list,
                                max_features=num_features,
                                ngram_range=(1,3),
                                max_df=0.7, min_df=3,
                                norm = 'l2')

    # use NMF model with the Frobenius norm
    implement_nmf = NMF(n_components=num_topics,
                        random_state=1,
                        solver='mu',
                        beta_loss='frobenius',
                        max_iter = 500)

    keys, output = [], []

    for i in index_dictionary.keys():
        keys.append(i)

    for key in keys:

        working_df = df.iloc[index_dictionary[key].values].copy()

        reviews = working_df['review']

        cleaned = clean_and_tokenize(reviews)

        working_df['cleaned_reviews'] = cleaned

        transform = vectorizer.fit_transform(working_df['cleaned_reviews'])
        transform_array = transform.toarray()

        # Non-negative matrix factorization (NMF) implementation W*H = original matrix
        # https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.NMF.html

        W = implement_nmf.fit_transform(transform_array)
        #H = implement_nmf.components_

        topics =  display_topics(vectorizer, implement_nmf, W, working_df, num_top_words, num_top_reviews)

        output.append(topics)

    return output
