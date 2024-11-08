import pandas as pd
import numpy as np


def readFile(file):
    series = pd.read_excel(file, header=0, index_col=0, parse_dates=True)
    pd.Series.shape
    if not pd.api.types.is_datetime64_any_dtype(series.index):
        series.index = pd.to_datetime(series.index, dayfirst=True)

    NEMBA = series[series.iloc[:, 0] == 'E012NEMBA']
    PZP001 = series[series.iloc[:, 0] == 'E012MAPZP001']
    PZP002 = series[series.iloc[:, 0] == 'E012MAPZP002']
    PZP003 = series[series.iloc[:, 0] == 'E012MAPZP003']
    PCVP001 = series[series.iloc[:, 0] == 'E012MAPCVP001']
    PCVP002 = series[series.iloc[:, 0] == 'E012MAPCVP002']
    PCVP004 = series[series.iloc[:, 0] == 'E012MAPCVP004']

    NEMBA = NEMBA.iloc[:, 1]
    PZP001 = PZP001.iloc[:, 3]
    PZP002 = PZP002.iloc[:, 3]
    PZP003 = PZP003.iloc[:, 3]
    PCVP001 = PCVP001.iloc[:, 3]
    PCVP002 = PCVP002.iloc[:, 3]
    PCVP004 = PCVP004.iloc[:, 3]

    NEMBA.index = NEMBA.index.normalize()
    PZP001.index = PZP001.index.normalize()
    PZP002.index = PZP002.index.normalize()
    PZP003.index = PZP003.index.normalize()
    PCVP001.index = PCVP001.index.normalize()
    PCVP002.index = PCVP002.index.normalize()
    PCVP004.index = PCVP004.index.normalize()

    DATA_P2 = DATAP2(PZP001, PZP002, PZP003, PCVP001, PCVP002, PCVP004)
    DATA_P3 = DATAP3(DATA_P2)
    Nemba_Ma = NEMBAMa(NEMBA, DATA_P3)
    DATA_P4 = pd.concat((Nemba_Ma['NEMBA'], DATA_P3), axis=1)

    res = transform(DATA_P4)
    return res


def PCVDataFrame(PCVP001, PCVP002, PCVP004):
    DATA_PCV = pd.DataFrame({
        'PCVP001': PCVP001,
        'PCVP002': PCVP002,
        'PCVP004': PCVP004
        })
    df = DATA_PCV.copy()

    for i in range(len(df) - 1, - 1, - 1):
        if pd.isnull(df.iloc[i]['PCVP004']):
            df.iloc[i]['PCVP004'] = round(df.iloc[i + 1]['PCVP004'] *
                                          (1 + (df.iloc[i]['PCVP002'] -
                                                df.iloc[i + 1]['PCVP002']) /
                                           df.iloc[i]['PCVP002']), 2)
    DATA_PCV_ad = df.copy()
    return DATA_PCV_ad


def PZDataFrame(PZP001, PZP002, PZP003):
    DATA_PZ = pd.DataFrame({
        'PZP001': PZP001,
        'PZP002': PZP002,
        'PZP003': PZP003
    })
    return DATA_PZ


def DATAP2(PZP001, PZP002, PZP003, PCVP001, PCVP002, PCVP004):
    DATA_PCV_ad = PCVDataFrame(PCVP001, PCVP002, PCVP004)
    DATA_PZ = PZDataFrame(PZP001, PZP002, PZP003)
    first_record_date = DATA_PCV_ad['PCVP001'].first_valid_index()

    DATA_P2 = pd.concat([DATA_PCV_ad, DATA_PZ], axis=1)
    DATA_P2_f = DATA_P2.loc[first_record_date:]

    return DATA_P2_f


def DATAP3(DATA_P2_f):
    DATA_P3 = DATA_P2_f.copy()
    time_windows = pd.Timedelta(days=35)

    DATA_P3 = fill_na_within_window(DATA_P3, time_windows)

    df = DATA_P3.copy()
    merged_df = merge_close_readings(df)
    res = merged_df.copy()

    return res


def NEMBAMa(NEMBA, DATA_P3):
    df = pd.DataFrame(NEMBA)
    df.rename(columns={df.columns[0]: 'NEMBA'}, inplace=True)
    # Calculate the rolling mean with a window of 3, 7 & 14
    df['N_MEAN_3'] = df['NEMBA'].rolling(window=3).mean()
    df['N_MEAN_7'] = df['NEMBA'].rolling(window=7).mean()
    df['N_MEAN_14'] = df['NEMBA'].rolling(window=14).mean()
    df['N_MAX_3'] = df['NEMBA'].rolling(window=3).max()
    df['N_MAX_7'] = df['NEMBA'].rolling(window=7).max()
    df['N_MAX_14'] = df['NEMBA'].rolling(window=14).max()

    DATA_P3.index = DATA_P3.index.normalize()
    df = df[~df.index.duplicated()]
    df = df.reindex(DATA_P3.index)

    return df


def fill_na_within_window(df, time_window):
    for column in df.columns:
        for i in range(len(df)):
            if pd.isna(df.iloc[i][column]):
                current_date = df.index[i]
                window_start = current_date - time_window
                window_end = current_date + time_window

                # Find the first valid value within the time window
                valid_values = df[column][window_start:window_end].dropna()
                if not valid_values.empty:
                    df.at[current_date, column] = valid_values.iloc[0]
    return df


def merge_close_readings(df, days_threshold=7):
    merged_data = []
    current_group = []
    current_dates = []

    for i in range(len(df)):
        if i == 0:
            current_group.append(df.iloc[i])
            current_dates.append(df.index[i])
        else:
            if (df.index[i] - df.index[i - 1]).days < days_threshold:
                current_group.append(df.iloc[i])
                current_dates.append(df.index[i])
            else:
                if current_group:
                    mean_values = np.mean(current_group, axis=0)
                    mean_date = np.mean([d.timestamp() for d in current_dates])
                    mean_date = pd.to_datetime(mean_date, unit='s')
                    merged_data.append((mean_date, mean_values))
                current_group = [df.iloc[i]]
                current_dates = [df.index[i]]

    if current_group:
        mean_values = np.mean(current_group, axis=0)
        mean_date = np.mean([d.timestamp() for d in current_dates])
        mean_date = pd.to_datetime(mean_date, unit='s')
        merged_data.append((mean_date, mean_values))

    merged_df = pd.DataFrame({date: values for date, values in merged_data}).T
    merged_df.columns = df.columns
    merged_df.index.name = 'Fecha'

    return merged_df


def transform(df):
    nemba = df['NEMBA'].values
    newNemba = []

    pcvp4 = df['PCVP004'].values
    newPcvp4 = pcvp4[5:]

    for i in range(len(nemba) - 5):
        sublista = nemba[i:i + 5]
        newNemba.append(sublista)

    df_Pablo = pd.DataFrame({
        'NEMBA': newNemba,
        'PCVP004': newPcvp4
    })
    return df_Pablo


if __name__ == '__main__':
    res = readFile('damdata_danador_data.xlsx')
    print(res)
