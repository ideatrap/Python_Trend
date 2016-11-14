

api_key = "Bu5FzXgzNNcpmLvykAbw"

import quandl
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')



def state_list():
    fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return fiddy_states[0][0][1:]


def grab_initial_state_data():
    states = state_list()

    main_df = pd.DataFrame()

    for abbv in states:
        query = "FMAC/HPI_" + str(abbv)
        df = quandl.get(query, authtoken=api_key)
      #  print(query)
        df = df.rename(columns={'Value': abbv})
        df[abbv] = (df[abbv] - df[abbv][0]) / df[abbv][0] * 100.0
       # print(df.head())
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)

    pickle_out = open("fiddy_states3.pickle", 'wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()



def HPI_Benchmark():
    df = quandl.get("FMAC/HPI_USA", authtoken=api_key)
    df["United States"] = (df["United States"] - df["United States"][0]) / df["United States"][0] * 100.0
    return df

#fig = plt.figure()
ax1 = plt.subplot2grid((2, 1), (0, 0))
ax2 = plt.subplot2grid((2,1),(1,0), sharex = ax1)

HPI_data = pd.read_pickle('fiddy_states3.pickle')




#Adding new moving average data to the set
HPI_data['TX12MA'] = HPI_data['TX'].rolling(12).mean()
HPI_data['TX12STD'] = HPI_data['TX'].rolling(12).std()
#HPI_data['TX1yr'] = HPI_data['TX'].resample('A').mean()

TX_AK_12corr = pd.rolling_corr(HPI_data['TX'], HPI_data['AK'],12)


#HPI_data.fillna(value = -99999, inplace = True)
#HPI_data.dropna(how = 'any', inplace=True)


#print(HPI_data[['TX', 'TX1yr']])


#TX1yr = HPI_data['TX'].resample('A').ohlc()

HPI_data['TX'].plot(ax = ax1, label ="TX HPI")
#HPI_data['TX12MA'].plot(ax = ax1)
HPI_data['AK'].plot(ax = ax1, label ="AK HPI")


TX_AK_12corr.plot(ax=ax2)
#HPI_data['TX12STD'].plot()



#HPI_data['TX'].plot(ax=ax1)
#TX1yr.plot(color = 'k', ax=ax1)

#plt.legend().remove()
plt.show()
