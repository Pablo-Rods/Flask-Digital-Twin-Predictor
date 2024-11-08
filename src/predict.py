import pathlib
import joblib as jb
import numpy as np
import matplotlib.pyplot as plt

from src.readData import readFile


def randomForest(file, min, seed):
    df = readFile(file)
    model = jb.load(pathlib.Path('models', 'new_model.joblib'))

    X = np.stack(df['NEMBA'])
    X_flat = X.reshape(X.shape[0], -1)
    X_flat.reshape(-1, 1)

    predictions = model.predict(X_flat)

    plot_results(df, predictions, min, seed)

    return predictions


def plot_results(df, prediction, min, seed):
    x1 = []
    c = 0
    for e in df['NEMBA']:
        x1.append(c)
        c = c+1

    y = df['PCVP004'].values

    plt.subplot(2, 1, 2)
    plt.plot(y, label='Actual PCVP004 (Test)', color='blue')
    plt.plot(prediction,
             label='Predicted PCVP004 (Test)', color='red', linestyle='--')
    plt.title('Random Forest Regression: Testing Set')
    plt.xlabel('Time')
    plt.ylabel('PCVP004')
    plt.legend()
    plt.grid(True)

    plt.savefig('./static/images/'+seed+'.png')
