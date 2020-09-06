from datetime import datetime

import logging
from dateutil import parser
from flask import Flask, abort, jsonify, request

from lib.fan import Fan
from lib.humidify import Humidify
from lib.metrics import Metrics
from lib.growing import Growing
from flask_cors import CORS

from lib.properties import Property

m = Metrics()
g = Growing()
p = Property()
app = Flask(__name__)
cors = CORS(app)
fan = Fan()
h = Humidify()


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.route('/api/metrics/<metric>')
def metrics(metric):
    labels = []
    data = []

    range_data = m.get_metric_range_data(metric)
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

        if day_count != g.get_growing_day_count():
            g.set_day_counter(day_count)

    if data.get('sunrise'):
        try:
            sunrise = parser.parse(data['sunrise']).time()
        except Exception as e:
            logging.error(e)
            return abort(400, description="Incorrect value '{}' for sunrise".format(data['sunrise']))

        g.set_sunrise(sunrise)

    if data.get('day_length_hours'):
        try:
            day_length_hours = int(data['day_length_hours'])
        except Exception as e:
            logging.error(e)
            return abort(400, description="Incorrect value '{}' for day_length_hours".format(data['day_length_hours']))

        g.set_day_length_hours(day_length_hours)

    if data.get('sunrise_duration_minutes'):
        try:
            sunrise_duration_minutes = int(data['sunrise_duration_minutes'])
        except Exception as e:
            logging.error(e)
            return abort(400, description="Incorrect value '{}' for sunrise_duration_minutes".format(data['sunrise_duration_minutes']))

        g.set_sunrise_duration_minutes(sunrise_duration_minutes)

    if data.get('sunset_duration_minutes'):
        try:
            sunset_duration_minutes = int(data['sunset_duration_minutes'])
        except Exception as e:
            logging.error(e)
            return abort(400, description="Incorrect value '{}' for sunset_duration_minutes".format(data['sunset_duration_minutes']))

        g.set_sunset_duration_minutes(sunset_duration_minutes)

    return g.get_all_info()


@app.route('/api/fan')
def fan_get():
    return fan.get_all_info()


@app.route('/api/fan', methods=['POST'])
def fan_update():
    data = request.json

    if not data:
        return {}, 204

    if data.get('manual_mode'):
        fan.set_manual_mode(True)
    else:
        fan.set_manual_mode(False)

    if data.get('fan_speed') and data['fan_speed'] != p.get_property_value(fan.get_fan_speed()):
        fan.set_fan_speed_property(data.get('fan_speed'))

    return fan.get_all_info()


@app.route('/api/humidify')
def humidify_get():
    return h.get_all_info()


@app.route('/api/humidify', methods=['POST'])
def humidify_update():
    data = request.json

    if not data:
        return {}, 204

    if data.get('is_disabled'):
        h.disable()
    else:
        h.enable()

    if data.get('manual_mode'):
        h.set_manual_mode(True)
    else:
        h.set_manual_mode(False)

    if data.get('pump_usage_interval'):
        h.set_pump_usage_interval(data.get('pump_usage_interval'))

    if data.get('pump_duration'):
        h.set_pump_duration(data.get('pump_duration'))

    if data.get('manual_humidity') and data.get('manual_mode'):
        h.set_manual_humidity(data.get('manual_humidity'))

    return h.get_all_info()
