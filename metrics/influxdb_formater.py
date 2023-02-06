# pylint: disable=R0903
class MetricsInfluxdbFormater:
    @staticmethod
    def format_dict(measurement_name, values, date, **filters):
        """
        Format a dictionary with the format key:value
        :param measurement_name: Messurement name for the influx db
        :param values: the dictionary with the format <status_id:count>
        :param date: the date of the measurement
        :param filter: the filters used to obtain this messurement
        :return: A formated string
        """
        filter_str = ','.join([f"{key}={value}" for key, value in filters.items()])
        values_str = ','.join([f"{key}={value}" for key, value in values.items()])
        return f"{measurement_name} {filter_str} {values_str} {date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')}"
