import pandas as pd
import datetime
#import pandas.io.data as web
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')

start = datetime.datetime(1920, 1, 1)
end = datetime.datetime(2016, 12, 31)

# dateframe
#df = web.DataReader("XOM", "yahoo", start, end)
#print(df)



df = pd.read_csv("SPY.txt", index_col=0)
#df.set_index('Date',inplace= True)

df2 = df.pct_change()
df3 = df - df[0]
print(df2.head())


df2['Close'].plot()
plt.legend()
plt.show()

