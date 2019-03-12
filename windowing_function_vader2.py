import pandas as pd
from sklearn import preprocessing
import pickle as pckl
import numpy as np

max_abs_scaler = preprocessing.MaxAbsScaler()


def window_df(df, params):

    upvote_window, percent_window, total_window = [], [], []

    window_unix = params['window_days'] * 86400

    # set the shift for taking the derivative, 1 if none given
    try:
        shift = params['shift']
    except:
        shift = 1


    for i in range(len(df)):

        window_close = int(df['time_of_review_unix'].iloc[i])
        window_start = window_close - window_unix

        min_index = min(df.index[df['time_of_review_unix'].between(window_start,
                                                                   window_close,
                                                                   inclusive=True)].tolist())


        #upvotes_in_period = df['upvotes'].iloc[i] - df['upvotes'].iloc[min_index]
        #upvote_window.append(upvotes_in_period)

        if min_index > 0:

            upvotes_in_period = df['upvotes'].iloc[i] - df['upvotes'].iloc[min_index]
            upvote_window.append(upvotes_in_period)

            total_votes_period = df['total_votes'].iloc[i] - df['total_votes'].iloc[min_index]
            total_window.append(total_votes_period)

            percent_window.append(upvotes_in_period/total_votes_period)

            #single_deriv = percent_window - percent_window.shift(shift)
            #deriv = pd.DataFrame({'deriv': single_deriv})

        else:

            upvotes_in_period = df['upvotes'].iloc[i]
            upvote_window.append(upvotes_in_period)

            total_window.append(i+1)

            percent_window.append(df['upvotes'].iloc[i]/(i+1))


    window_df = df[['time_of_review', 'review', 'upvoted', 'time_of_review_unix', 'minutes_played']].copy()
    window_df['upvotes_window'] = upvote_window
    window_df['total_window'] = total_window
    window_df['percent_window'] = percent_window

    percent_window_series = window_df['percent_window']
    roc = percent_window_series - percent_window_series.shift(shift)
    deriv = pd.DataFrame({'deriv': roc})
    norm_deriv = max_abs_scaler.fit_transform(deriv)

    window_df['norm_deriv'] = norm_deriv

    full_df = window_df.fillna(value=0)

    if params['save_df'] == True:
        pckl.dump(full_df, open('{0}_{1}day_window_df.pckl'.format(params['game'], params['window_days']), 'wb'))
    else:
        pass
    #min_window_moving = min(window_moving)

#    window_df = pd.DataFrame({'time_of_review': df['time_of_review'].tolist(),
#                              'reviews': df['review'].tolist(),
#                              'upvoted': df['upvoted'].tolist(),
#                              'upvotes_window': upvote_window,
#                              'total_window': total_window,
#                              'percent_window': percent_window,
#                              'norm_deriv': norm_deriv,
#                              'time_of_review_unix': df['time_of_review_unix'].tolist(),
#                              'minutes_played': df['minutes_played'].tolist()})

    return full_df


def window_vader(df, params):

    #comp_sent_raw_sum, comp_sent_nostop_sum = [], []
    comp_sent_raw_window, comp_sent_nostop_window = [], []

    window_unix = params['window_days'] * 86400

    #comp_sent_raw = df['comp_sent_raw']
    #comp_sent_nostop = df['comp_sent_nostop']


    # set the shift for taking the derivative, 1 if none given
    try:
        shift = params['shift']
    except:
        shift = 1


    for i in range(len(df)):

        window_close = int(df['time_of_review_unix'].iloc[i])
        window_start = window_close - window_unix

        min_index = min(df.index[df['time_of_review_unix'].between(window_start,
                                                                   window_close,
                                                                   inclusive=True)].tolist())

        #print(min_index)

        current_window_size = i - min_index + 1


        #comp_sent_raw_period = df['comp_sent_raw'].iloc[i] - df['comp_sent_raw'].iloc[min_index]
        #omp_sent_nostop_period = df['comp_sent_nostop'].iloc[i] - df['comp_sent_nostop'].iloc[min_index]

        #comp_sent_raw_period = max(df['comp_sent_raw'].iloc[min_index:i].cumsum())
        #print(comp_sent_raw_period)
        #comp_sent_max = max(comp_sent_raw_period)
        #print(type(comp_sent_max), comp_sent_max)
        #comp_sent_nostop_period = max(df['comp_sent_nostop'].iloc[min_index:i].cumsum())

        #comp_sent_raw_sum.append(comp_sent_raw_period)
        #comp_sent_nostop_sum.append(comp_sent_nostop_period)

        if i > 0:

            comp_sent_raw_period = max(df['comp_sent_raw'].iloc[min_index:i].cumsum())
            comp_sent_nostop_period = max(df['comp_sent_nostop'].iloc[min_index:i].cumsum())

            comp_sent_raw_window.append(comp_sent_raw_period/current_window_size)
            comp_sent_nostop_window.append(comp_sent_nostop_period/current_window_size)

        else:
            comp_sent_raw_window.append(df['comp_sent_raw'].iloc[0]/1)
            comp_sent_nostop_window.append(df['comp_sent_nostop'].iloc[0]/1)

    #print(comp_sent_raw_window[0:10])

    #print('length of window', len(comp_sent_raw_window), 'length of df', print(len(df)))

    df['comp_sent_raw_window'] = comp_sent_raw_window
    df['comp_sent_nostop_window'] = comp_sent_nostop_window

    return df




def deriv_window(df, params, column):

    window_unix = params['window_days'] * 86400

    roc_window = []

    try:
        shift = params['shift']
    except:
        shift = 1

    roc = (df[column] - df[column].shift(1)).fillna(value=0)


    for i in range(len(df)):

        window_close = int(df['time_of_review_unix'].iloc[i])
        window_start = window_close - window_unix

        min_index = min(df.index[df['time_of_review_unix'].between(window_start,
                                                                   window_close,
                                                                   inclusive=True)].tolist())

        current_window_size = i - min_index + 1


        if i > 0:

            deriv_period = max(df[column].iloc[min_index:i].cumsum())

            roc_window.append(deriv_period/current_window_size)

        else:

            deriv_period = 0

            roc_window.append(deriv_period/current_window_size)

    new_column = column + '_roc'

    deriv = pd.DataFrame({'deriv': roc_window})
    norm_deriv = preprocessing.maxabs_scale(deriv)

    df[new_column] = norm_deriv
    new_df = df

    return new_df
