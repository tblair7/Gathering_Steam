import pandas as pd
from sklearn import preprocessing
import pickle as pckl
import numpy as np

max_abs_scaler = preprocessing.MaxAbsScaler()


def window_df(df, params):

    upvote_window, percent_window, total_window = [], [], []

    window_unix = int(int(params['window_days']) * 86400)



    for i in range(len(df)):

        window_close = int(df['time_of_review_unix'].iloc[i])
        window_start = int(window_close - window_unix)

        min_index = int(min(df.index[df['time_of_review_unix'].between(window_start,
                                                                   window_close,
                                                                   inclusive=True)].tolist()))


        #upvotes_in_period = df['upvotes'].iloc[i] - df['upvotes'].iloc[min_index]
        #upvote_window.append(upvotes_in_period)

        if i > 0:

            upvotes_in_period = df['upvotes'].iloc[i] - df['upvotes'].iloc[min_index]
            upvote_window.append(upvotes_in_period)

            total_votes_period = df['total_votes'].iloc[i] - df['total_votes'].iloc[min_index]
            total_window.append(total_votes_period)

            percent_window.append(upvotes_in_period/total_votes_period)

            #single_deriv = percent_window - percent_window.shift(shift)
            #deriv = pd.DataFrame({'deriv': single_deriv})

        else:

            upvotes_in_period = df['upvotes'].iloc[0]
            upvote_window.append(upvotes_in_period)

            total_window.append(i+1)

            percent_window.append(df['upvotes'].iloc[0]/1)


    window_df = df[['time_of_review', 'review', 'upvoted', 'time_of_review_unix']].copy()
    window_df['upvotes_window'] = upvote_window
    window_df['total_window'] = total_window
    window_df['percent_window'] = percent_window

    percent_window_series = window_df['percent_window']
    #roc = percent_window_series - percent_window_series.shift(1)
    #deriv = pd.DataFrame({'deriv': roc})
    #norm_deriv = preprocessing.maxabs_scale(deriv)

    #window_df['upvote_roc'] = norm_deriv

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


def sent_window(df, params):

    #comp_sent_raw_sum, comp_sent_nostop_sum = [], []
    neu_window, neg_window, pos_window, comp_window = [], [], [], []

    window_unix = params['window_days'] * 86400

    #new_df = df.copy()

    #comp_sent_raw = df['comp_sent_raw']
    #comp_sent_nostop = df['comp_sent_nostop']


    # set the shift for taking the derivative, 1 if none given


    for i in range(len(df)):

        window_close = int(df['time_of_review_unix'].iloc[i])
        window_start = int(window_close - window_unix)

        min_index = int(min(df.index[df['time_of_review_unix'].between(window_start, window_close, inclusive=True)].tolist()))

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

            #print('min index', min_index, 'i', i, max(df['neu_sent'].iloc[min_index:i].cumsum()))

            neu_period = max(df['neu_sent'].iloc[min_index:i].cumsum())
            neg_period = max(df['neg_sent'].iloc[min_index:i].cumsum())
            pos_period = max(df['pos_sent'].iloc[min_index:i].cumsum())
            comp_period = max(df['comp_sent'].iloc[min_index:i].cumsum())

            neu_window.append(neu_period/current_window_size)
            neg_window.append(neg_period/current_window_size)
            pos_window.append(pos_period/current_window_size)
            comp_window.append(comp_period/current_window_size)


        else:
            neu_window.append(df['neu_sent'].iloc[0]/current_window_size)
            neg_window.append(df['neg_sent'].iloc[0]/current_window_size)
            pos_window.append(df['pos_sent'].iloc[0]/current_window_size)
            comp_window.append(df['comp_sent'].iloc[0]/current_window_size)
            #comp_sent_nostop_window.append(df['comp_sent_nostop'].iloc[0]/1)

    print(type(min(df.index[df['time_of_review_unix'].between(window_start,
                                                               window_close,
                                                               inclusive=True)].tolist())))

    #print('length of window', len(comp_sent_raw_window), 'length of df', print(len(df)))

    df['neu_window'] = pd.Series(neu_window)#/max(neu_window)
    df['neg_window'] = pd.Series(neg_window)#/max(neg_window)
    df['pos_window'] = pd.Series(pos_window)#max(pos_window)
    df['comp_window'] = pd.Series(comp_window)#/max(comp_window)
    #df['comp_sent_nostop_window'] = comp_sent_nostop_window

    new_df = df.copy()

    return new_df




def deriv_window(df, params, columns):

    window_unix = int(params['window_days'] * 86400)

    for column in columns:

        roc_window = []

        roc = (df[column] - df[column].shift(1)).fillna(value=0)


        for i in range(len(df)):

            window_close = int(df['time_of_review_unix'].iloc[i])
            window_start = int(window_close - window_unix)

            min_index = int(min(df.index[df['time_of_review_unix'].between(window_start,
                                                                       window_close,
                                                                       inclusive=True)].tolist()))

            current_window_size = int(i - min_index + 1)


            if i > 0:

                deriv_period = int(max(df[column].iloc[min_index:i].cumsum()))

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


def deriv_full_window(df, params, columns):

    window_unix = params['window_days'] * 86400

    new_df = df.copy()


    for column in columns:

        roc_window = []

        #roc = (df[column] - df[column].shift(1)).fillna(value=0)


        for i in range(len(df)):

            window_close = int(df['time_of_review_unix'].iloc[i])
            window_start = window_close - window_unix

            min_index = min(df.index[df['time_of_review_unix'].between(window_start,
                                                                       window_close,
                                                                       inclusive=True)].tolist())

            current_window_size = i - min_index + 1


            if i > 0:

                deriv_period = df[column].iloc[i] - df[column].iloc[min_index]

                roc_window.append(deriv_period/current_window_size)

            else:

                deriv_period = 0

                roc_window.append(deriv_period/current_window_size)

        new_column = column + '_fullroc'

        deriv = pd.DataFrame({'deriv': roc_window})
        norm_deriv = preprocessing.maxabs_scale(deriv)

        new_df[new_column] = norm_deriv


    return new_df


def delta_percent(df, days):

    #window_unix = params['window_days'] * 86400

    new_df = df.copy()

    for day in days:

        window_unix = int(day) * 86400

        delta_percent = []

        for i in range(len(df)):

            window_close = int(df['time_of_review_unix'].iloc[i])
            window_start = int(window_close - window_unix)

            min_index = min(df.index[df['time_of_review_unix'].between(window_start,
                                                                       window_close,
                                                                       inclusive=True)].tolist())

            if i > 0:

                delta_percent.append(df['percent_window'].iloc[i] - df['percent_window'].iloc[min_index])

            else:
                delta_percent.append(0)

        day_string = str(day) + 'day_delta'

        new_df[day_string] = delta_percent


    return new_df

def forecast(df, days):

    new_df = df.copy()

    window_unix = int(days * 86400)

    delta_forecast = []

    for i in range(len(df)):
        window_start = int(df['time_of_review_unix'].iloc[i])
        window_close = int(window_start + window_unix)

        max_index = max(df.index[df['time_of_review_unix'].between(window_start,
                                                                   window_close,
                                                                   inclusive=True)].tolist())

        delta_forecast.append(df['percent_window'].iloc[max_index] - df['percent_window'].iloc[i])

    day_string = str(days) + 'day_forecast'

    new_df[day_string] = delta_forecast

    return new_df
