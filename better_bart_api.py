from flask import Flask, request

import station_logic

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello world!'


@app.route('/stations')
def get_stations():
    return station_logic.get_stations(bart_api_key=request.headers.get('X-API-KEY'))


if __name__ == "__main__":
    app.run()