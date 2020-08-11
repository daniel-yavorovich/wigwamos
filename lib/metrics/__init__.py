import logging

from prometheus_api_client.prometheus_connect import PrometheusConnect


class Metrics:
    def __init__(self):
        self.prom = PrometheusConnect()

    def __get_avg_value(self, metric, last):
        try:
            result = self.prom.custom_query(
                query='sum(sum_over_time({metric}[{last}]))/sum(count_over_time({metric}[{last}]))'.format(
                    metric=metric,
                    last=last))
            return float(result[0]['value'][1])
        except Exception as e:
            logging.error(e)
            return None

    def get_avg_soil_moisture(self, last='5m'):
        return self.__get_avg_value('soil_moisture', last)

    def get_avg_humidity(self, last='5m'):
        return self.__get_avg_value('air_humidity', last)

    def get_avg_temperature(self, last='1m'):
        return self.__get_avg_value('air_temperature', last)
