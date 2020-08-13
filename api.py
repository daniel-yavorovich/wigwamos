from datetime import datetime

from flask import Flask, abort, jsonify
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


@app.route('/api/growing')
def growing():
    period = g.get_current_period()
    config = period.config
    day_count = g.get_growing_day_count()
    total_days = g.get_growing_total_days()

    return {
        'config': config.name,
        'period': period.name,
        'day_count': day_count,
        'total_days': total_days
    }
