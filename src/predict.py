import pathlib
import numpy as np
import joblib as jb
import pandas as pd
import matplotlib.pyplot as plt

from tensorflow.keras.models import load_model  # type: ignore
from statsmodels.tsa.seasonal import seasonal_decompose


def create_sequences(data, sequence_length, target_columns):
    sequences = []
    labels = []
    for i in range(len(data) - sequence_length):
        sequence = data.iloc[i:i + sequence_length].values
        label = data.iloc[i + sequence_length][target_columns].values
        sequences.append(sequence)
        labels.append(label)
    return np.array(sequences), np.array(labels)


def readFile(file):
    series = pd.read_excel(file, header=0, index_col=0, parse_dates=True)

    time_window = pd.Timedelta(days=35)
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

    PCV_data = pd.DataFrame({
        'PCVP001': PCVP001,
        'PCVP002': PCVP002,
        'PCVP004': PCVP004
        })
    PZ_data = pd.DataFrame({
        'PZP001': PZP001,
        'PZP002': PZP002,
        'PZP003': PZP003
    })

    NEMBA_data = pd.DataFrame({
        'NEMBA': NEMBA
    })

    PCV_data = eliminate_nulls(PCV_data)

    data = pd.concat([NEMBA_data, PZ_data, PCV_data], axis=1)

    first_record_date = data['PCVP001'].first_valid_index()
    data = data.loc[first_record_date:]

    data = fill_na_within_window(data, time_window)
    return data


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


def eliminate_nulls(df):
    for i in range(len(df) - 1, - 1, - 1):
        if pd.isnull(df.iloc[i]['PCVP004']):
            df.iloc[i]['PCVP004'] = round(df.iloc[i + 1]['PCVP004'] *
                                          (1 + (df.iloc[i]['PCVP002'] -
                                                df.iloc[i + 1]['PCVP002']) /
                                           df.iloc[i]['PCVP002']), 2)

    return df


def predict(file):
    df = readFile(file)[['NEMBA', 'PZP001', 'PZP002', 'PZP003']]

    loaded_model = load_model(pathlib.Path('models', 'lstm_model.h5'))
    loaded_scaler = jb.load(pathlib.Path('models', 'scaler.pkl'))

    scaled_df = loaded_scaler.transform(df)

    target_columns = ['PZP001', 'PZP002', 'PZP003']
    X, Y = create_sequences(pd.DataFrame(scaled_df, columns=df.columns), 100,
                            target_columns)

    predictions = loaded_model.predict(X)

    return predictions


def randomForest(file, min):
    df = readFile(file)[['NEMBA', 'PCVP004']]

    nemba_decompose = seasonal_decompose(df['NEMBA'], model='additive',
                                         period=6)
    nemba_trend = nemba_decompose.trend.interpolate().dropna()
    nemba_seasonal = nemba_decompose.seasonal.interpolate().dropna()
    nemba_residual = nemba_decompose.resid.interpolate().dropna()

    nemba_trend = nemba_trend[-min:]
    nemba_seasonal = nemba_seasonal[-min:]
    nemba_residual = nemba_residual[-min:]

    model = jb.load(pathlib.Path('models', 'random_forest.joblib'))

    X = np.column_stack((nemba_trend.values, nemba_seasonal.values,
                         nemba_residual.values))

    predictions = model.predict(X)

    plot_results(df, min, predictions)

    return predictions


def plot_results(df, min_length, prediction):
    plt.subplot(2, 1, 2)
    plt.plot(df.index[-min_length:], prediction,
             label='Predicted PCVP004 (Test)', color='red', linestyle='--')
    plt.title('Random Forest Regression: Testing Set')
    plt.xlabel('Time')
    plt.ylabel('PCVP004')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    prediction = randomForest(pathlib.Path
                              ('Data', 'damdata_danador_data.xlsx'), 730)
    print(prediction)
