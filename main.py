import yfinance as yf
import pandas as pd
import numpy as np
from pandas import DataFrame
from pandas.tseries.offsets import DateOffset
import matplotlib.pyplot as plt

vix_df = yf.download('^VIX')

"""вычисление скользящей средней за 30 дней через оконную функцию rolling"""
vix_df['MA'] = vix_df['Close'].rolling('30D').mean()

"""фильтруем значения: цена закрытия выше на 50% МА"""
vix_df_filter = vix_df[vix_df.Close > 1.5 * vix_df.MA]

"""
diff() разница значений 
Переводим дни в число и фильтруем значения >= 30 
"""
boolean_mask = pd.Series(vix_df_filter.index).diff() / np.timedelta64(1, 'D') >= 30
boolean_mask[0] = True

signals = vix_df_filter[boolean_mask.values]

sp_df = yf.download('^GSPC', start='1990-01-01')

test_ = sp_df[(sp_df.index >= signals.index[0]) &
              (sp_df.index <= signals.index[0] + DateOffset(months=6))]

a = (test_.Close.pct_change() + 1).prod()
b = test_['Close'].pct_change().sum()

returns = []
for i in range(len(signals)):
    subdf = sp_df[(sp_df.index >= signals.index[i]) &
                  (sp_df.index <= signals.index[i] + DateOffset(months=6))]
    returns.append(subdf['Close'].pct_change().sum() * 100)
    # returns.append((subdf.Close.pct_change()+1).prod())
# print(returns)
pd.DataFrame(returns, index=signals.index.date).plot(kind='bar')
"""Для полного отображения даты по оси Х"""
plt.tight_layout()
plt.show()
