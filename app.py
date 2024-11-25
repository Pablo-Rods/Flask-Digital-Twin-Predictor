from dotenv import load_dotenv
from flask import Flask, request
from flasgger import Swagger

from src.predict import predict

load_dotenv()

app = Flask(__name__)
swagger = Swagger(app)


@app.route('/predict/', methods=['POST'])
def get_data():
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
    prediction = predict(data)
    res = f"PCVP004: {prediction}"

    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
