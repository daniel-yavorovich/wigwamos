from datetime import datetime

import logging

import re
from flask import Flask, abort, jsonify, request
from lib.metrics import Metrics
from lib.growing import Growing
from flask_cors import CORS

m = Metrics()
g = Growing()
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.route('/api/metrics/<metric>')
def metrics(metric):
    labels = []
    data = []

    range_data = m.get_metric_range_data(metric_name=metric)
    if not range_data:
        abort(404, description="Metric not found")

    for i in range_data[0]['values']:
        labels.append(datetime.fromtimestamp(i[0]).strftime('%H:%M'))
        data.append(i[1])

    return {
        'labels': labels,
        'data': data,
        'avg': m.get_avg_value(metric)
    }


@app.route('/api/growing/configs')
def growing_configs():
    return {'names': g.get_config_names()}


@app.route('/api/growing')
def growing_get():
    return g.get_all_info()


@app.route('/api/growing', methods=['POST'])
def growing_update():
    data = request.json

    if not data:
        return {}, 204

    if data.get('config'):
        if data['config'] not in g.get_config_names():
            return abort(400, description="Config {} unavailable".format(data['config']))
        else:
            g.set_current_config(data['config'])

    if data.get('day_count'):
        try:
            day_count = int(data['day_count'])
        except Exception as e:
            logging.error(e)
            return abort(400, description="Incorrect value '{}' for day_count".format(data['day_count']))

        if 0 > day_count > 100:
            return abort(400, description="Value '{}' for day_count out of range 1..100".format(data['day_count']))

        g.set_day_counter(day_count)

    if data.get('manual_mode'):
        if re.search('false', data.get('manual_mode'), re.IGNORECASE):
            g.set_manual_mode(False)
        else:
            g.set_manual_mode(True)

    return g.get_all_info()
