import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from matplotlib.dates import DateFormatter
from sklearn import preprocessing


def plot(df, params, columns):

    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    yearsFmt = mdates.DateFormatter('%Y')



    date = df['time_of_review'].iloc[1000:]

    plot_list = []

    for column in columns:
        plot_list.append('date, ' + df[column].iloc[1000:])

    plot_string = ','.join(plot_list)



    #ax = plt.figure(figsize=(20,10))
    fig, ax = plt.subplots(figsize=(20,10))

    ax.plot(plot_string)

    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)

    fig.legend(columns, loc='upper right', bbox_to_anchor=(0.8, 0.15))

    plt.ylabel('Normalized arb units')
    plt.title('ARK in {0}-day Periods Over Time'.format(params['window_days']))

    plt.show()

    fig.savefig('{0}_{1}days_window_plot.png'.format(params['game'], params['window_days']))

#def plot_reviews_roc(df, game, window_days):

#    max_abs_scaler = preprocessing.MaxAbsScaler()
#    np_scaled = max_abs_scaler.fit_transform(c['weighted_deriv'].iloc[200:].reshape(-1,1))
