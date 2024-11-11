import joblib as jb
import numpy as np

import pathlib
import json


def predict(data):
    array = json2Array(data)
    inputs = np.array([array])

    model = jb.load(pathlib.Path('models', 'new_model.joblib'))
    res = model.predict(inputs)

    return res


def json2Array(data):
    e = json.dumps(data)
    Nemba = json.loads(e)
    res = [np.array(val) for val in Nemba["NEMBA"]]

    return res
