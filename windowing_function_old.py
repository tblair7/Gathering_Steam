import pandas as pd
from sklearn import preprocessing
import pickle as pckl

max_abs_scaler = preprocessing.MaxAbsScaler()

def window_df(df, game, window_days, save_data, *args):

    upvote_window = []
    percent_window = []
    total_window = []

    #roc = [] # rate of change
    window_moving = []

    window_unix = window_days * 86400

    # set the shift for taking the derivative, 1 if none given
    try:
        shift = args[0]
    except:
        shift = 1


    for i in range(len(df)):

        window_close = df['time_of_review_unix'].iloc[i]
        window_start = window_close - window_unix

        min_index = min(df.index[df['time_of_review_unix'].between(window_start,
                                                                   window_close,
                                                                   inclusive=True)].tolist())


        upvotes_in_period = df['upvotes'].iloc[i] - df['upvotes'].iloc[min_index]
        upvote_window.append(upvotes_in_period)

        if i > 0:

            total_votes_period = df['total_votes'].iloc[i] - df['total_votes'].iloc[min_index]
            total_window.append(total_votes_period)

            percent_window.append(upvotes_in_period/total_votes_period)

            #single_deriv = percent_window - percent_window.shift(shift)
            #deriv = pd.DataFrame({'deriv': single_deriv})

        else:

            total_window.append(1)
            percent_window.append(df['upvotes'].iloc[i]/1)

            #roc.append(0)

    print(len(upvote_window), len(total_window), len(percent_window))
    #time_of_review_unix = df['time_of_review_unix']
    #mins_played = df['minutes_played']

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

    if save_df == True:
        pckl.dump(full_df, open('{0}_{1}day_window_df.pckl'.format(game, window_days), 'wb'))
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
