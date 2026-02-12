import pandas as pd
import yfinance as yf

ticker = "GC=F"
gcfdata = yf.download(ticker, period="26y", interval="1d")
gcfdata = gcfdata.reset_index()
gcfdata['Date'] = pd.to_datetime(gcfdata['Date']).dt.strftime('%m/%d/%Y')
print(gcfdata.head())
gcfdata.to_csv(r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\Gold.csv',index = False)

#%%
url = r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\Gold.csv'
gcfdata = pd.read_csv(url)
gcfdata['Date'] = pd.to_datetime(gcfdata['Date'])
gcfdata = gcfdata.sort_values('Date').set_index('Date')
gcfdata_filled = gcfdata.resample('D').ffill().reset_index()
print(gcfdata_filled.head())
gcfdata_filled.to_csv(r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\Gold_Resampled.csv', index = False)