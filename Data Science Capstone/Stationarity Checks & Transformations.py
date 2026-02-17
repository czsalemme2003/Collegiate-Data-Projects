import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.dates as mdates
import sys

url = r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\Final_Macro_Economic_Dataset.csv'
df = pd.read_csv(url)
print(df.head())
#plotting
plt.figure(figsize=(12,6))
plt.plot(df.index, df['EFFR'], color='blue', label='EFFR')
plt.xlabel("Date")
plt.ylabel("Effective Federal Funds Rate (%)")
plt.title("Effective Federal Funds Rate Over Time")
plt.legend()
plt.grid(True)
plt.show()

#rolling mean and variance plots
effr_rolling_mean = df.EFFR.rolling(window = 100).mean()
effr_rolling_variance = df.EFFR.rolling(window = 100).var()
plt.subplots(2,1, figsize = (10,6), sharex=True)
fig, axes = plt.subplots(2,1, figsize = (10,6), sharex=True)
axes[0].plot(effr_rolling_mean, color = "blue")
axes[0].set_title(f"EFFR - Rolling Mean")
axes[0].set_xlabel("Magnitude")
axes[0].set_ylabel("Samples")
axes[1].plot(effr_rolling_variance, color = "red")
axes[1].set_title(f"EFFR - Rolling Variance ")
axes[1].set_xlabel("Magnitude")
axes[1].set_ylabel("Samples")
plt.tight_layout()
plt.show()

#%% Stationarity Test ADF & KPSS
from statsmodels.tsa.stattools import adfuller
def ADF_Cal(x):
    result = adfuller(x)
    print("ADF Statistic: %f" %result[0])
    print('p-value: %f' % result[1])
    print('Critical Values:')
    for key, value in result[4].items():
        print('\t%s: %.3f' % (key, value))

ADF_Cal(df['EFFR'])

from statsmodels.tsa.stattools import kpss
def kpss_test(x):
    print ('Results of KPSS Test:')
    kpsstest = kpss(x, regression='c', nlags="auto")
    kpss_output = pd.Series(kpsstest[0:3], index=['Test Statistic','p-value','Lags Used'])
    for key,value in kpsstest[3].items():
        kpss_output['Critical Value (%s)'%key] = value
    print (kpss_output)
kpss_test(df['EFFR'])

#both of these tests ran confirmed from the rolling mean and variance plots that the EFFR is nonstationary -- meaning we have to transform the data
#ADF ==> H0 Series has a unit root (Non-Stationary), p-value: 0.423Fail to reject $H_0$. Data is Non-Stationary.
#KPSS ==> Series is trend stationary (Stationary), p-value: 0.010Reject $H_0$., Data is Non-Stationary.
#The KPSS warning ("actual p-value is smaller than the p-value returned") indicates that your test statistic (2.166) is so far beyond the 1% critical value (0.739) that the data is very strongly non-stationary.

#%% differentiation
diff1 = df['EFFR'].diff()
diff1 = diff1.fillna(0)
print(diff1)
kpss_test(diff1)
#%% diff2
diff2 = diff1.diff()
diff2 = diff2.fillna(0)
kpss_test(diff2)
#%%
diff1_rolling_mean = diff1.rolling(window = 100).mean()
diff1_rolling_var = diff1.rolling(window = 100).var()
plt.subplots(2,1, figsize = (10,6), sharex=True)
#rolling mean and var plot
fig, axes = plt.subplots(2,1, figsize = (10,6), sharex=True)
axes[0].plot(diff1_rolling_mean, color = "blue")
axes[0].set_title(f"EFFR - 1st Order Differencing - Rolling Mean")
axes[0].set_xlabel("Magnitude")
axes[0].set_ylabel("Samples")
axes[1].plot(diff1_rolling_var, color = "red")
axes[1].set_title(f"EFFR - 1st Order Differencing - Rolling Variance ")
axes[1].set_xlabel("Magnitude")
axes[1].set_ylabel("Samples")
plt.tight_layout()
plt.show()

#%%#reg plot
plt.figure(figsize=(12,6))
plt.plot(diff2, color = 'blue')
plt.title("EFFR First Order Differencing")
plt.grid(True)
plt.show()
#%% log
log= np.log(df['EFFR'])
kpss_test(log)
#%% Best for Stationarity after trial, error and research that suggests log tranformation and a first order differencing
#is the best for financial data
log_diff1 = np.diff(log)
kpss_test(log_diff1)
plt.figure(figsize=(12,6))
plt.plot(log_diff1, color = 'blue')
plt.title("EFFR Log Transformation")
plt.grid(True)
plt.show()
#%%
log_diff1_series = pd.Series(log_diff1)
log_diff1_rolling_mean = log_diff1_series.rolling(window = 100).mean()
log_diff1_rolling_var = log_diff1_series.rolling(window = 100).var()
fig, axes = plt.subplots(2,1, figsize = (10,6), sharex=True)
axes[0].plot(log_diff1_rolling_mean, color = "blue")
axes[0].set_title(f"EFFR - 1st Order Differencing & Log - Rolling Mean")
axes[0].set_xlabel("Magnitude")
axes[0].set_ylabel("Samples")
axes[1].plot(log_diff1_rolling_var, color = "red")
axes[1].set_title(f"EFFR - 1st Order Differencing & Log- Rolling Variance ")
axes[1].set_xlabel("Magnitude")
axes[1].set_ylabel("Samples")
plt.tight_layout()
plt.show()
#%%
print(log_diff1_series.head())
log_diff1_series.to_csv(r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\Transformations.csv', index = false)