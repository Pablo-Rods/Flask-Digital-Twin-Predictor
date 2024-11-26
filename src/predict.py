import joblib as jb
import numpy as np

import pathlib
import json


def predict(data):
    array = json2Array(data)
    inputs = np.array([array])
    res = []

    model = jb.load(pathlib.Path('models', 'new_model.joblib'))

    for i in range(len(inputs)):
        prediction = model.predict(inputs[i])
        res.append(prediction)

    return res


def json2Array(data):
    e = json.dumps(data)
    Nemba = json.loads(e)
    res = Nemba["NEMBA"]
    newNemba = []
    for i in range(len(res) - 4):
        sublista = res[i:i + 5]
        newNemba.append(sublista)

    X_3d = np.array(newNemba)

    return X_3d
