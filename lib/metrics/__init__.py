import logging

from prometheus_api_client.prometheus_connect import PrometheusConnect


class Metrics:
    def __init__(self):
        self.prom = PrometheusConnect()

    def get_avg_soil_moisture(self, last='5m'):
        try:
            result = self.prom.custom_query(
                query='sum(sum_over_time(soil_moisture[{last}]))/sum(count_over_time(soil_moisture[{last}]))'.
                    format(last=last))
            return float(result[0]['value'][1])
        except Exception as e:
            logging.error(e)
            return 0

    def is_need_watering(self):
        return self.get_avg_soil_moisture() == 1.0
