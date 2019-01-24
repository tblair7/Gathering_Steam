from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd

vader = SentimentIntensityAnalyzer()

def raw_sentiment(df):

    reviews = df['review']

    neu_sent = []
    neg_sent = []
    pos_sent = []
    comp_sent = []

    for review in reviews:
        score = vader.polarity_scores(review)

        neu_sent.append(score['neu'])
        neg_sent.append(score['neg'])
        pos_sent.append(score['pos'])
        comp_sent.append(score['compound'])

    df['neu_sent'] = neu_sent
    df['neg_sent'] = neg_sent
    df['pos_sent'] = pos_sent
    df['comp_sent'] = comp_sent

    return df



def no_stop_sentiment(df):

    reviews = df['tokenized_review']

    neu_sent = []
    neg_sent = []
    pos_sent = []
    comp_sent = []

    for review in reviews:
        score = vader.polarity_scores(review)

        neu_sent.append(score['neu'])
        neg_sent.append(score['neg'])
        pos_sent.append(score['pos'])
        comp_sent.append(score['compound'])

    df['neu_sent_nostop'] = neu_sent
    df['neg_sent_nostop'] = neg_sent
    df['pos_sent_nostop'] = pos_sent
    df['comp_sent_nostop'] = comp_sent

    return df


def full_sentiment(df):

    reviews_raw = df['review']
    reviews_tokenized = df['tokenized_review']

    neu_sent_raw = []
    neg_sent_raw = []
    pos_sent_raw = []
    comp_sent_raw = []

    neu_sent_nostop = []
    neg_sent_nostop = []
    pos_sent_nostop = []
    comp_sent_nostop = []

    for review in reviews_raw:
        score_raw = vader.polarity_scores(review)

        neu_sent_raw.append(score_raw['neu'])
        neg_sent_raw.append(score_raw['neg'])
        pos_sent_raw.append(score_raw['pos'])
        comp_sent_raw.append(score_raw['compound'])

    for review in reviews_tokenized:
        score_nostop= vader.polarity_scores(review)

        neu_sent_nostop.append(score_nostop['neu'])
        neg_sent_nostop.append(score_nostop['neg'])
        pos_sent_nostop.append(score_nostop['pos'])
        comp_sent_nostop.append(score_nostop['compound'])


    df['neu_sent_nostop'] = neu_sent_nostop
    df['neg_sent_nostop'] = neg_sent_nostop
    df['pos_sent_nostop'] = pos_sent_nostop
    df['comp_sent_nostop'] = comp_sent_nostop

    df['neu_sent_raw'] = neu_sent_raw
    df['neg_sent_raw'] = neg_sent_raw
    df['pos_sent_raw'] = pos_sent_raw
    df['comp_sent_raw'] = comp_sent_raw

    return df
