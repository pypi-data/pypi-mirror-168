import json
from datetime import datetime
from datetime import timedelta


def get_keys_for_current_month_for_day_aggregation_from_given_time(time):
    """
    Give key month given by time - which are then used to aggregate data
    :param time: month to use
    :return: array containing keys for this month (including given time)
    """
    result = []
    end = time
    start = time.replace(day=1)
    while start <= end:
        result.append("{}-{}".format(start.month, start.day))
        start = start + timedelta(days=1)
    return result


def get_keys_for_current_month_for_day_aggregation():
    """
    Give key month given by time - which are then used to aggregate data
    :return: array containing keys for this month (including given time)
    """
    return get_keys_for_current_month_for_day_aggregation_from_given_time(datetime.now())


class MonthDataAvroHelperV1:

    def __init__(self, raw_input):
        """
        :param raw_input: the raw data which you would have got from DB or other place. This data will be used to do the
        aggregation
        e.g. This is a sample data which you will pass:
        {"updated_at":1663665518937,"days":{"9-17":1,"9-4":1,"9-18":1,"9-5":1,"9-15":1,"9-6":1}}
        """
        dict_data = json.loads(raw_input)
        self.days = dict_data["days"]

    def get_current_month_numeric_aggregation_from_now(self, aggregate=True, aggregation_key="days"):
        """
        This method will give you data for current month.

        :param aggregation_key:  days, days_hour [currently only days is supported]
        :param time: from [start of this month <--> current time]
        :param aggregate: aggregation or raw values
        :return: if aggregate=True, then single numeric value of the total, otherwise array of values
        """

        return self.get_current_month_numeric_aggregation_from_given_time(datetime.now(), aggregate, aggregation_key)

    def get_current_month_numeric_aggregation_from_given_time(self, time, aggregate=True, aggregation_key="days"):
        """
        This method will give you data for current month.

        :param aggregation_key:  days, days_hour [currently only days is supported]
        :param time: from [start of this month <--> the time given]
        :param aggregate: aggregation or raw values
        :return: if aggregate=True, then single numeric value of the total, otherwise array of values
        """

        # Find the keys
        keys = get_keys_for_current_month_for_day_aggregation_from_given_time(time)

        # Find data with all keys
        result = []
        for day in keys:
            try:
                if aggregation_key == "days":
                    result.append(self.days[day])
            except KeyError as error:
                pass

        # Give raw result or aggregated value
        if aggregate is False:
            return result
        else:
            sum = 0
            for i in result:
                sum = sum + i
            return sum
