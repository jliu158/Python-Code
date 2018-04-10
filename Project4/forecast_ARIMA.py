from pandas import read_csv
import pandas as pd
from math import log
from math import exp
from statsmodels.tsa.arima_model import ARIMA


series = read_csv('GDP.csv', header=0, parse_dates=[0], index_col=0)
GDP = series['GDP']
history = []
for i in GDP:
    history.append([log(i)])

final_result = []
year_list = []

for i in range(2030-2015):
    model = ARIMA(history, order=(2,2,2))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    history.append([yhat])
    final_result.append(exp(yhat))
    year_list.append(2015+i)

dataframe = pd.DataFrame({'Year':year_list, 'GDP': final_result})
print dataframe

dataframe.to_csv('GDP_new.csv', index=False)