import pandas as pd
import numpy as np


def gen(df, sentiment_dict, sent):


    output = []


    for dict in sentiment_dict:
        df_slice = df[['time_of_review', 'percent_window', 'review', 'pos_sent', 'neg_sent']].iloc[dict['group'].values].copy()


        working_df = df_slice.sort_values('time_of_review').groupby(df_slice['time_of_review'].dt.floor('D')).head(1)
        review_slice = df_slice[df_slice['review'].str.len() > 12]

        if sent == 'neg':
            review_example = review_slice.sort_values('neg_sent', ascending = False).groupby(review_slice['time_of_review'].dt.floor('D')).head(1)
            working_df['review_example'] = review_example['review'].values

        elif sent == 'pos':
            #review_example = df_slice.sort_values('pos_sent', ascending = False).groupby(df_slice['time_of_review'].dt.floor('D')).head(1)
            review_example = review_slice.sort_values('pos_sent', ascending = False).groupby(review_slice['time_of_review'].dt.floor('D')).head(1)
            working_df['review_example'] = review_example['review'].values


        topics = len(working_df)*[dict['topics']]

        working_df['topics'] = topics

        output.append(working_df)

    full_output = pd.concat(output)

    return full_output
