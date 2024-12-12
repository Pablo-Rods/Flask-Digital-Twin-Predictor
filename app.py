from dotenv import load_dotenv
from flask import Flask, request
from flasgger import Swagger
import numpy as np

from src.predict import predict

load_dotenv()

app = Flask(__name__)
swagger = Swagger(app)


@app.route('/predict/PCVP001', methods=['POST'])
def predict_PCVP001():
    """
    Predict PCVP001 value
    ---
    consumes:
        - application/json
    produces:
        - application/json
    parameters:
        - name: body
          in: body
          description: Array of the latest 5 NEMBA value
          required: true
          schema:
            type: object
            properties:
                NEMBA:
                    type: array
                    example: [708.48, 708.38, 708.33, 708.27, 708.3]
    responses:
        "200":
            description: OK
            content:
                application/json:
                    schema:
                    type: object
                    properties:
                        PCVP01:
                            type: float
                            example: 1.87
    """
    data = request.json
    prediction = predict(data, "PCVP001")
    array1 = np.array(prediction)
    array = np.array2string(array1, separator=',')

    return array


@app.route('/predict/PCVP002', methods=['POST'])
def predict_PCVP002():
    """
    Predict PCVP002 value
    ---
    consumes:
        - application/json
    produces:
        - application/json
    parameters:
        - name: body
          in: body
          description: Array of the latest 5 NEMBA value
          required: true
          schema:
            type: object
            properties:
                NEMBA:
                    type: array
                    example: [708.48, 708.38, 708.33, 708.27, 708.3]
    responses:
        "200":
            description: OK
            content:
                application/json:
                    schema:
                    type: object
                    properties:
                        PCVP02:
                            type: float
                            example: 1.87
    """
    data = request.json
    prediction = predict(data, "PCVP002")
    array1 = np.array(prediction)
    array = np.array2string(array1, separator=',')

    return array


@app.route('/predict/PCVP004', methods=['POST'])
def predict_PCVP004():
    """
    Predict PCVP004 value
    ---
    consumes:
        - application/json
    produces:
        - application/json
    parameters:
        - name: body
          in: body
          description: Array of the latest 5 NEMBA value
          required: true
          schema:
            type: object
            properties:
                NEMBA:
                    type: array
                    example: [708.48, 708.38, 708.33, 708.27, 708.3]
    responses:
        "200":
            description: OK
            content:
                application/json:
                    schema:
                    type: object
                    properties:
                        PCVP04:
                            type: float
                            example: 1.87
    """
    data = request.json
    prediction = predict(data, "PCVP004")
    array1 = np.array(prediction)
    array = np.array2string(array1, separator=',')

    return array


@app.route('/predict/PZP001', methods=['POST'])
def predict_PZP001():
    """
    Predict PZP001 value
    ---
    consumes:
        - application/json
    produces:
        - application/json
    parameters:
        - name: body
          in: body
          description: Array of the latest 5 NEMBA value
          required: true
          schema:
            type: object
            properties:
                NEMBA:
                    type: array
                    example: [708.48, 708.38, 708.33, 708.27, 708.3]
    responses:
        "200":
            description: OK
            content:
                application/json:
                    schema:
                    type: object
                    properties:
                        PZP001:
                            type: float
                            example: 1.87
    """
    data = request.json
    prediction = predict(data, "PZP001")
    array1 = np.array(prediction)
    array = np.array2string(array1, separator=',')

    return array


@app.route('/predict/PZP002', methods=['POST'])
def predict_PZP002():
    """
    Predict PZP002 value
    ---
    consumes:
        - application/json
    produces:
        - application/json
    parameters:
        - name: body
          in: body
          description: Array of the latest 5 NEMBA value
          required: true
          schema:
            type: object
            properties:
                NEMBA:
                    type: array
                    example: [708.48, 708.38, 708.33, 708.27, 708.3]
    responses:
        "200":
            description: OK
            content:
                application/json:
                    schema:
                    type: object
                    properties:
                        PZP002:
                            type: float
                            example: 1.87
    """
    data = request.json
    prediction = predict(data, "PZP002")
    array1 = np.array(prediction)
    array = np.array2string(array1, separator=',')

    return array


@app.route('/predict/PZP003', methods=['POST'])
def predict_PZP003():
    """
    Predict PZP003 value
    ---
    consumes:
        - application/json
    produces:
        - application/json
    parameters:
        - name: body
          in: body
          description: Array of the latest 5 NEMBA value
          required: true
          schema:
            type: object
            properties:
                NEMBA:
                    type: array
                    example: [708.48, 708.38, 708.33, 708.27, 708.3]
    responses:
        "200":
            description: OK
            content:
                application/json:
                    schema:
                    type: object
                    properties:
                        PZP003:
                            type: float
                            example: 1.87
    """
    data = request.json
    prediction = predict(data, "PZP003")
    array1 = np.array(prediction)
    array = np.array2string(array1, separator=',')

    return array


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
