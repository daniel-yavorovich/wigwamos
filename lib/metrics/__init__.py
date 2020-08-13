from datetime import timedelta, datetime
import logging

from prometheus_api_client.prometheus_connect import PrometheusConnect


class Metrics:
    DEFAULT_AVG_PERIOD = '10m'

    def __init__(self):
        self.prom = PrometheusConnect()

    def get_avg_value(self, metric_name, last=DEFAULT_AVG_PERIOD):
        try:
            result = self.prom.custom_query(
                query='sum(sum_over_time({metric_name}[{last}]))/sum(count_over_time({metric_name}[{last}]))'.format(
                    metric_name=metric_name,
                    last=last))
            return float(result[0]['value'][1])
        except Exception as e:
            logging.error(e)
            return None

    def get_avg_soil_moisture(self, last=DEFAULT_AVG_PERIOD):
        return self.get_avg_value('soil_moisture', last)

    def get_avg_humidity(self, last=DEFAULT_AVG_PERIOD):
        return self.get_avg_value('air_humidity', last)

    def get_avg_temperature(self, last=DEFAULT_AVG_PERIOD):
        return self.get_avg_value('air_temperature', last)

    def get_metric_range_data(self, metric_name: str,
                              label_config: dict = None,
                              start_time: datetime = (datetime.now() - timedelta(minutes=10)),
                              end_time: datetime = datetime.now(),
                              chunk_size: timedelta = timedelta(seconds=60),
                              store_locally: bool = False,
                              params: dict = None):

        return self.prom.get_metric_range_data(metric_name=metric_name, label_config=label_config,
                                               start_time=start_time, end_time=end_time,
                                               chunk_size=chunk_size, store_locally=store_locally,
                                               params=params)
