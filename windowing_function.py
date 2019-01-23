def window_df(df, window_days):

    import pandas as pd

    upvote_window = []
    percent_window = []
    total_window = []

    window_unix = window_days * 86400

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

        else:

            total_window.append(1)
            percent_window.append(df['upvotes'].iloc[i]/1)


    window_df = pd.DataFrame({'time_of_review': df['time_of_review'],
                              'reviews': df['review'],
                              'upvoted': df['upvoted'],
                              'upvotes_window': upvote_window,
                              'total_window': total_window,
                              'percent_window': percent_window,
                              'time_of_review_unix': df['time_of_review_unix'],
                              'minutes_played': df['minutes_played']})

    return window_df
