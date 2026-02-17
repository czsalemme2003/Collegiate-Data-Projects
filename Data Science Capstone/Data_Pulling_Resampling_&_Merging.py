import pandas as pd
import numpy as np
from fredapi import Fred
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
x=1
print(x)
#%% Pulling FRED
fred = Fred(api_key='87b82b8539bd67f9864fb8840b29cda0')
start_date = '2000-01-01'
end_date = '2025-12-31'
#fred
fred_series = {
    'EFFR': 'DFF',
    '3M_Treasury': 'DTB3',
    '2Y_Treasury': 'DGS2',
    '5Y_Treasury': 'DGS5',
    '10Y_Treasury': 'DGS10',
    '30Y_Treasury': 'DGS30',
    '6M_Treasury_Bill_Rate': 'DGS6MO',
    '3M_Treasury_Bill_Rate': 'DGS3MO',
    'ONRRP_Total_Securities_Sold': 'RRPONTTLD',
    'ONRRP_Total_Securities_Purchased': 'RPONTTLD',
    'SOFR': 'SOFR',
    'Crude_Oil_Price': 'DCOILWTICO' }
fred_data = pd.DataFrame({name: fred.get_series(code, observation_start=start_date, observation_end=end_date) for name, code in fred_series.items()})
fred_data.index = pd.to_datetime(fred_data.index)
#%% pulling yahoofinance
tickers = ['^GSPC', '^VIX', 'GC=F']
yahoo_data = {}
for ticker in tickers:
    df = yf.download(ticker, start=start_date, end=end_date)
    df.columns = [f"{ticker}_{col}" for col in df.columns]
    yahoo_data[ticker] = df
yahoo_combined = pd.concat(yahoo_data.values(), axis=1)
yahoo_combined.index = pd.to_datetime(yahoo_combined.index)
combined_data = pd.merge(fred_data, yahoo_combined, left_index=True, right_index=True, how='outer')
combined_data.to_csv("macro_market_data.csv", index=True)

print("✅ Data successfully saved as 'macro_market_data.csv'")
print("Shape of final dataset:", combined_data.shape)
print("Columns included:\n", combined_data.columns.tolist())

#%% Forward Fill  and resaving to csv
df = pd.read_csv(r'C:\Users\czsal\PycharmProjects\datscapstone\macro_market_data.csv')
print(df.head())
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')
df_filled = df.ffill()
df_filled.to_csv(r'C:\Users\czsal\PycharmProjects\datscapstone\Macro_Market_Data_Ready.csv', index=False)
#%% Plotting EFFR
plt.figure(figsize=(12,6))
plt.plot(combined_data.index, combined_data['EFFR'], color='blue', label='EFFR')
plt.xlabel("Date")
plt.ylabel("Effective Federal Funds Rate (%)")
plt.title("Effective Federal Funds Rate Over Time")
plt.legend()
plt.grid(True)
plt.show()
#%% CPI-U
file_path = r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\raw data\Consumer Price Index for All Urban Consumers (CPI-U).csv'
df_cpiu = pd.read_csv(file_path)
print(df_cpiu.head())
df_cpiu['Date'] = pd.to_datetime(df_cpiu['Date'])
df_cpiu = df_cpiu.sort_values('Date').set_index('Date')
df_cpiu_daily = df_cpiu[['Value', '12-Month % Change']].resample('D').ffill()
print(df_cpiu_daily.head())
end_of_month = df_cpiu_daily.index.max() + pd.offsets.MonthEnd(0)
df_cpiu_daily = df_cpiu_daily.reindex(pd.date_range(df_cpiu_daily.index.min(), end_of_month, freq='D')).ffill()
print(df_cpiu_daily.head())
df_cpiu_daily = df_cpiu_daily.reset_index().rename(columns={'index': 'Date'})
df_cpiu_daily['Date'] = df_cpiu_daily['Date'].dt.strftime('%m/%d/%Y')
df_cpiu_daily.to_csv('CPI_Daily_Resampled_Formatted.csv', index=False)
#%% Employment-Population Ratio
epr = r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\raw data\Employment-Population Ratio.xlsx'
df_epr = pd.read_excel(epr)
print(df_epr.head())
df_epr['Date'] = pd.to_datetime(df_epr['Date'])
df_epr = df_epr.sort_values('Date').set_index('Date')
print(df_epr.head())
df_epr_daily = df_epr.resample('D').ffill()
end_of_month = df_epr_daily.index.max() + pd.offsets.MonthEnd(0)
df_epr_daily = df_epr_daily.reindex(pd.date_range(df_epr_daily.index.min(), end_of_month, freq='D')).ffill()
print(df_epr_daily.head())
df_epr_daily = df_epr_daily.reset_index().rename(columns={'index': 'Date'})
df_epr_daily['Date'] = df_epr_daily['Date'].dt.strftime('%m/%d/%Y')
df_epr_daily.to_csv(r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\EP_Daily_Resampled.csv', index=False)
#%% CPI-W
cpiw_fp = r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\data\CPI-W.csv'
df_cpiw = pd.read_csv(cpiw_fp)
df_cpiw = df_cpiw.drop(columns = ['Series ID', 'Year', 'Period'] )
print(df_cpiw.head())
df_cpiw['Date'] = pd.to_datetime(df_cpiw['Label'], format='%Y %b')
df_cpiw = df_cpiw.sort_values('Date').set_index('Date')
df_cpiw = df_cpiw.drop(columns = ['Label'])
df_cpiw_daily = df_cpiw[['Value', '12-Month % Change']].resample('D').ffill()
print(df_cpiw.head())
end_of_month = df_cpiw_daily.index.max() + pd.offsets.MonthEnd(0)
df_cpiw_daily = df_cpiw_daily.reindex(pd.date_range(df_cpiw_daily.index.min(), end_of_month, freq='D')).ffill()
print(df_cpiw_daily.head())
df_cpiw_daily = df_cpiw_daily.reset_index().rename(columns={'index': 'Date'})
df_cpiw_daily['Date'] = df_cpiw_daily['Date'].dt.strftime('%m/%d/%Y')
df_cpiw_daily.to_csv('CPIW_Resampled_Formatted.csv', index=False)
#%% PPI_FD
ppifd_fp = r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\data\PPI_FD.csv'
df_ppifd = pd.read_csv(ppifd_fp)
df_ppifd = df_ppifd.drop(columns = ['Series ID', 'Year', 'Period'])
print(df_ppifd.head())
df_ppifd['Date'] = pd.to_datetime(df_ppifd['Label'], format='%Y %b')
df_ppifd = df_ppifd.sort_values('Date').set_index('Date')
df_ppifd = df_ppifd.drop(columns = ['Label'])
df_ppifd_daily = df_ppifd[['Value', '1-Month % Change','12-Month % Change']].resample('D').ffill()
print(df_ppifd_daily.head())
last_date - df_ppifd.index.max()
end_of_month = last_date + pd.offsets.MonthEnd(0)
all_days = pd.date_range(start = df_ppifd.index.min(), end = end_of_month, freq='D')
df_ppifd_daily = df_ppifd.reindex(all_days).ffill()
df_ppifd_final = df_ppifd_daily.reset_index().rename(columns={'index': 'Date'})
df_ppifd_final['Date'] = df_ppifd_final['Date'].dt.strftime('%m/%d/%Y')
df_ppifd_final.to_csv(r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\PPIFD_Resampled_Formatted.csv', index=False)
#%% PPI_AC
ppiac_fp = r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\data\PPI_AC.csv'
df_ppiac = pd.read_csv(ppiac_fp)
df_ppiac = df_ppiac.drop(columns = ['Series ID', 'Year', 'Period'])
print(df_ppiac.head())
df_ppiac['Date'] = pd.to_datetime(df_ppiac['Label'], format='%Y %b')
df_ppiac = df_ppiac.sort_values('Date').set_index('Date')
df_ppiac = df_ppiac.drop(columns = ['Label'])
df_ppiac_daily = df_ppiac[['Value', '1-Month % Change','12-Month % Change']].resample('D').ffill()
print(df_ppiac_daily.head())
last_date = df_ppiac.index.max()
end_of_month = last_date + pd.offsets.MonthEnd(0)
all_days = pd.date_range(start = df_ppiac.index.min(), end = end_of_month, freq='D')
df_ppiac_daily = df_ppiac_daily.reindex(all_days).ffill()
df_ppiac_final = df_ppiac_daily.reset_index().rename(columns={'index': 'Date'})
df_ppiac_final['Date'] = df_ppiac_final['Date'].dt.strftime('%m/%d/%Y')
df_ppiac_final.to_csv(r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\PPIAC_Resampled_Formatted.csv', index=False)
#%% Unemployment Rate
ur_fp = r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\data\Unemployment Rate.csv'
df_ur = pd.read_csv(ur_fp)
df_ur = df_ur.drop(columns = ['Series ID', 'Year', 'Period'])
print(df_ur.head())
df_ur['Date'] = pd.to_datetime(df_ur['Label'], format='%Y %b')
df_ur = df_ur.sort_values('Date').set_index('Date')
df_ur = df_ur.drop(columns = ['Label'])
df_ur_daily = df_ur['Value'].resample('D').ffill()
print(df_ur_daily.head())
last_date = df_ur.index.max()
end_of_month = last_date + pd.offsets.MonthEnd(0)
all_days = pd.date_range(start = df_ur.index.min(), end = end_of_month, freq = 'D')
df_ur_daily = df_ur_daily.reindex(all_days).ffill()
df_ur_final = df_ur_daily.reset_index().rename(columns={'index': 'Date'})
df_ur_final['Date'] = df_ur_final['Date'].dt.strftime('%m/%d/%Y')
df_ur_final.to_csv(r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\Unemployment_Rate_Resampled_Formatted.csv', index=False)
#%% CLFPC
clfpc_fp = r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\data\CLFPC.csv'
clfpc = pd.read_csv(clfpc_fp)
clfpc = clfpc.drop(columns = ['Series ID', 'Year', 'Period'])
print(clfpc.head())
clfpc['Date'] = pd.to_datetime(clfpc['Label'], format='%Y %b')
clfpc = clfpc.sort_values('Date').set_index('Date')
clfpc = clfpc.drop(columns = ['Label'])
clfpc_daily = clfpc['Value'].resample('D').ffill()
print(clfpc_daily.head())
last_date = clfpc.index.max()
end_of_month = last_date + pd.offsets.MonthEnd(0)
all_days = pd.date_range(start=clfpc.index.min(), end=end_of_month, freq='D')
clfpc_daily = clfpc_daily.reindex(all_days).ffill()
clfpc_final = clfpc_daily.reset_index().rename(columns={'index': 'Date'})
clfpc_final['Date'] = clfpc_final['Date'].dt.strftime('%m/%d/%Y')
clfpc_final.to_csv(r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\CLFPC_Resampled_Formatted.csv', index=False)
#%% PCE
pce_path = r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\data\PCE.csv'
pce = pd.read_csv(pce_path)
pce['observation_date'] = pd.to_datetime(pce['observation_date'])
pce = pce.sort_values('observation_date').set_index('observation_date')
pce_daily = pce.resample('D').ffill()
print(pce_daily.head())
last_date = pce.index.max()
end_of_month = last_date + pd.offsets.MonthEnd(0)
all_days = pd.date_range(start=pce.index.min(), end=end_of_month, freq='D')
pce_daily = pce_daily.reindex(all_days).ffill()
pce_final = pce_daily.reset_index().rename(columns={'index': 'Date'})
pce_final['Date'] = pce_final['Date'].dt.strftime('%m/%d/%Y')
pce_final.to_csv(r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\PCE_Resampled_Formatted.csv', index = False)
#%% PCEPI
pcepi_path = r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\data\PCEPI (1).csv'
pcepi = pd.read_csv(pcepi_path)
pcepi['observation_date'] = pd.to_datetime(pcepi['observation_date'])
pcepi = pcepi.sort_values('observation_date').set_index('observation_date')
pcepi_daily = pcepi.resample('D').ffill()
end_of_month = pcepi.index.max() + pd.offsets.MonthEnd(0)
pcepi_daily = pcepi_daily.reindex(pd.date_range(pcepi_daily.index.min(), end_of_month, freq='D')).ffill()
print(pcepi_daily.head())
pcepi_daily = pcepi_daily.reset_index().rename(columns={'index': 'Date'})
pcepi_daily['Date'] = pcepi_daily['Date'].dt.strftime('%m/%d/%Y')
pcepi_daily.to_csv(r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\PCEPI_Resampled_Formatted.csv', index = False)
#%% M2
m2_path = r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\raw data\M2SL.csv'
m2 = pd.read_csv(m2_path)
m2['observation_date'] = pd.to_datetime(m2['observation_date'])
m2 = m2.sort_values('observation_date').set_index('observation_date')
m2_daily = m2.resample('D').ffill()
end_of_month = m2.index.max() + pd.offsets.MonthEnd(0)
m2_daily = m2_daily.reindex(pd.date_range(m2_daily.index.min(), end_of_month, freq='D')).ffill()
print(m2_daily.head())
m2_daily = m2_daily.reset_index().rename(columns={'index': 'Date'})
m2_daily['Date'] = m2_daily['Date'].dt.strftime('%m/%d/%Y')
m2_daily.to_csv(r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\M2_Resampled_Formatted.csv', index = False)
#%%  WEI
import openpyxl
url = r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\raw data\WEI.xlsx'
wei = pd.read_excel(url)
print(wei.head())
wei['observation_date'] = pd.to_datetime(wei['observation_date'])
wei = wei.sort_values('observation_date').set_index('observation_date')
wei_daily = wei.resample('D').ffill()
print(wei_daily.head(20))
wei_final = wei_daily.reset_index().rename(columns={'observation_date' : 'Date'})
wei_final['Date'] = wei_final['Date'].dt.strftime('%m/%d/%Y')
wei_final.to_csv(r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\WEI_Resampled_Formatted.csv', index = False)
#%% Collateralization of Currency - Securities Pledged (RESPPNTEPPNWW)
respnnteppnww = r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\raw data\RESPPNTEPPNWW.csv'
securities_pledged = pd.read_csv(respnnteppnww)
print(securities_pledged.head())
securities_pledged['observation_date'] = pd.to_datetime(securities_pledged['observation_date'])
securities_pledged = securities_pledged.sort_values('observation_date').set_index('observation_date')
securities_pledged_daily = securities_pledged.resample('D').ffill()
print(securities_pledged_daily.head())
securities_pledged_final = securities_pledged_daily.reset_index().rename(columns={'observation_date' : 'Date'})
securities_pledged_final.to_csv(r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\RESPNNTEPPNWW_Resampled_Formatted.csv')
#%% Collateralization of Currency - Gold Certificate Account (RESPPNGNWW)
resppngnww = r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\raw data\RESPPNGNWW.csv'
gold_certificate = pd.read_csv(resppngnww)
print(gold_certificate.head())
gold_certificate['observation_date'] = pd.to_datetime(gold_certificate['observation_date'])
gold_certificate = gold_certificate.sort_values('observation_date').set_index('observation_date')
gold_certificate_daily = gold_certificate.resample('D').ffill()
print(gold_certificate_daily.head())
gold_certifiate_final = gold_certificate_daily.reset_index().rename(columns={'observation_date' : 'Date'})
gold_certifiate_final.to_csv(r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\RESPPNGNWWW_Resampled_Formatted.csv')
#%% Collateralization of Currency - Federal Reserve Notes (RESPPNNWW)
resppnnww = r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\raw data\RESPPNNWW.csv'
reserve_notes = pd.read_csv(resppnnww)
print(reserve_notes.head())
reserve_notes['observation_date'] = pd.to_datetime(reserve_notes['observation_date'])
reserve_notes = reserve_notes.sort_values('observation_date').set_index('observation_date')
reserve_notes_daily = reserve_notes.resample('D').ffill()
print(reserve_notes_daily.head())
reserve_notes_final = reserve_notes_daily.reset_index().rename(columns={'observation_date' : 'Date'})
reserve_notes_final.to_csv(r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\RESPPNNWW_Resampled_Formatted.csv')
#%% Collateralization of Currency - Other Assets Pledged RESPPNONWW
respnonww = r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\raw data\RESPPNONWW.csv'
other_notes = pd.read_csv(respnonww)
print(other_notes.head())
other_notes['observation_date'] = pd.to_datetime(other_notes['observation_date'])
other_notes = other_notes.sort_values('observation_date').set_index('observation_date')
other_notes_daily = other_notes.resample('D').ffill()
print(other_notes_daily.head())
other_notes_final = other_notes_daily.reset_index().rename(columns={'observation_date' : 'Date'})
other_notes_final.to_csv(r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\RESPPNONWW_Resampled_Formatted.csv')
#%% Collateralization of Currency - Special Drawing Rights Certificate Account  (RESPPNSNWW)
respnnsnww = r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\raw data\RESPPNSNWW.csv'
special_drawing = pd.read_csv(respnnsnww)
print(special_drawing.head())
special_drawing['observation_date'] = pd.to_datetime(special_drawing['observation_date'])
special_drawing = special_drawing.sort_values('observation_date').set_index('observation_date')
special_drawing_daily = special_drawing.resample('D').ffill()
print(special_drawing_daily.head())
special_drawing_final = special_drawing_daily.reset_index().rename(columns={'observation_date' : 'Date'})
special_drawing_final.to_csv(r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\RESPPNSNWW_Resampled_Formatted.csv')
#%% PAYEMS
url = r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\raw data\PAYEMS.csv'
payemsdata = pd.read_csv(url)
print(payemsdata.head())
payemsdata['observation_date'] = pd.to_datetime(payemsdata['observation_date'])
payems = payemsdata.sort_values('observation_date').set_index('observation_date')
end_of_month = payems.index.max() + pd.offsets.MonthEnd(0)
payems_daily = payems.reindex(pd.date_range(payems.index.min(), end_of_month, freq='D')).ffill()
print(payems_daily.head())
payems_final = payems_daily.reset_index().rename(columns={'index' : 'observation_date'})
print(payems_final.head())
payems_final['observation_date'] = payems_final['observation_date'].dt.strftime('%m/%d/%Y')
payems_final.to_csv(r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\PAYEMS_Resampled_Formatted.csv')
#%% UMich Consumer Sentiment
url = r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\raw data\UMCSENT.csv'
umcsent = pd.read_csv(url)
print(umcsent.head())
umcsent['observation_date'] = pd.to_datetime(umcsent['observation_date'])
umcsent = umcsent.sort_values('observation_date').set_index('observation_date')
end_of_month = umcsent.index.max() + pd.offsets.MonthEnd(0)
umcsent_daily = umcsent.reindex(pd.date_range(umcsent.index.min(), end_of_month, freq='D')).ffill()
print(umcsent_daily.head())
umcesent_final = umcsent_daily.reset_index().rename(columns={'index' : 'observation_date'})
umcesent_final['observation_date'] = umcesent_final['observation_date'].dt.strftime('%m/%d/%Y')
umcesent_final.to_csv(r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\UMCSENT_Resampled_Formatted.csv', index = False)
#%% Inflation Expectations
url = r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\raw data\UMIE.csv'
umcie = pd.read_csv(url)
print(umcie.head())
umcie['observation_date'] = pd.to_datetime(umcie['observation_date'])
umcie = umcie.sort_values('observation_date').set_index('observation_date')
end_of_month = umcie.index.max() + pd.offsets.MonthEnd(0)
umcie_daily = umcie.reindex(pd.date_range(umcie.index.min(), end_of_month, freq='D')).ffill()
print(umcie_daily.head())
umcie_final = umcie_daily.reset_index().rename(columns={'index' : 'observation_date'})
umcie_final['observation_date'] = umcie_final['observation_date'].dt.strftime('%m/%d/%Y')
umcie_final.to_csv(r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\UMCIE_Resampled_Formatted.csv', index = False)
#%% NFCI
url = r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\raw data\nfci-data-series-csv.csv'
ncfi = pd.read_csv(url)
print(ncfi.head())
ncfi['Friday_of_Week'] = pd.to_datetime(ncfi['Friday_of_Week'])
ncfi = ncfi.sort_values('Friday_of_Week').set_index('Friday_of_Week')
ncfi_daily = ncfi.resample('D').ffill()
print(ncfi_daily.head(10))
ncfi_final = ncfi_daily.reset_index().rename(columns={'Friday_of_Week' : 'Date'})
print(ncfi_final)
ncfi_final.to_csv(r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\NCFI_Resampled_Formatted.csv')
#%% merging of resampled data
file_configs = [
    (r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\CLFPC_Resampled_Formatted.csv', {'Value': 'CLFPC'}),
    (r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\CPI_Daily_Resampled_Formatted.csv', {'Value': 'CPI', '12-Month % Change': 'CPI_12Mo_Change'}),
    (r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\CPIW_Resampled_Formatted.csv', {'Value': 'CPIW', '12-Month % Change': 'CPIW_12Mo_Change'}),
    (r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\EP_Daily_Resampled.csv', {'Value': 'EP'}),
    (r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\M2_Resampled_Formatted.csv', {}),
    (r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\NCFI_Resampled_Formatted.csv', {}),
    (r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\PAYEMS_Resampled_Formatted.csv', {}),
    (r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\PCE_Resampled_Formatted.csv', {}),
    (r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\PPIAC_Resampled_Formatted.csv', {'Value': 'PPIAC', '12-Month % Change': 'PPIAC_12Mo_Change', '1-Month % Change': 'PPIAC_1Mo_Change'}),
    (r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\PPIFD_Resampled_Formatted.csv', {'Value': 'PPIFD', '12-Month % Change': 'PPIFD_12Mo_Change', '1-Month % Change': 'PPIFD_1Mo_Change'}),
    (r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\RESPNNTEPPNWW_Resampled_Formatted.csv', {}),
    (r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\RESPPNGNWWW_Resampled_Formatted.csv', {}),
    (r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\RESPPNNWW_Resampled_Formatted.csv', {}),
    (r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\RESPPNONWW_Resampled_Formatted.csv', {}),
    (r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\RESPPNSNWW_Resampled_Formatted.csv', {}),
    (r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\UMCIE_Resampled_Formatted.csv', {'MICH': 'UMCIE'}),
    (r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\UMCSENT_Resampled_Formatted.csv', {}),
    (r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\Unemployment_Rate_Resampled_Formatted.csv', {'Value': 'Unemployment_Rate'}),
    (r'C:\Users\czsal\PycharmProjects\DataScienceCapstone\resampled data\WEI_Resampled_Formatted.csv', {})

]

dataframes = []

for file_path, rename_map in file_configs:
    df = pd.read_csv(file_path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    possible_date_cols = ['Date', 'observation_date']
    date_col = next((c for c in possible_date_cols if c in df.columns), None)

    if date_col is None:
        print(f"Warning: No date column found in {file_path}. Columns are: {df.columns.tolist()}")
        continue
    df[date_col] = pd.to_datetime(df[date_col])
    if rename_map:
        df = df.rename(columns=rename_map)
    df = df.set_index(date_col)
    df.index.name = 'Date'
    dataframes.append(df)
merged_df = pd.concat(dataframes, axis=1, join='outer')
merged_df = merged_df.sort_index().reset_index()
merged_df.to_csv('Merged_Economic_Data.csv', index=False)
print("Merge complete. Dimensions:", merged_df.shape)
print(merged_df.head())
#%% final merge
market_df = pd.read_csv('Macro_Market_Data_Ready.csv')
economic_df = pd.read_csv('Merged_Economic_Data.csv')
market_df['Date'] = pd.to_datetime(market_df['Date'])
economic_df['Date'] = pd.to_datetime(economic_df['Date'])
final_df = pd.merge(market_df, economic_df, on='Date', how='outer')
final_df = final_df.sort_values('Date').reset_index(drop=True)
final_df.to_csv('Final_Macro_Economic_Dataset.csv', index=False)

print("Merge complete!")
print(f"Final dataset dimensions: {final_df.shape}")
print(final_df.head())