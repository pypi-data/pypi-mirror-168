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


def get_keys_for_n_days_for_day_aggregation(time, days):
    """
    Give key from given time to N days - you can use these keys to get data from avro data

    :param time: time to start
    :param days: no of days
    :return: array containing keys for past N days (including given time)
    """
    result = []
    end = time
    start = time - timedelta(days=days)
    while start < end:
        start = start + timedelta(days=1)
        result.append("{}-{}".format(start.month, start.day))
    return result


class MonthDataAvroHelperV1:

    def __init__(self, raw_input):
        """
        :param raw_input: the raw data which you would have got from DB or other place. This data will be used to do the
        aggregation
        e.g. This is a sample data which you will pass:
        {"updated_at":1663665518937,"days":{"9-17":1,"9-4":1,"9-18":1,"9-5":1,"9-15":1,"9-6":1}}
        """
        dict_data = json.loads(raw_input)

        if dict_data.get("days") is not None:
            self.days = dict_data["days"]
        else:
            self.days = {}

        if dict_data.get("days_hours") is not None:
            self.days_hours = dict_data["days_hours"]
        else:
            self.days_hours = {}

        if dict_data.get("hours") is not None:
            self.hours = dict_data["hours"]
        else:
            self.hours = {}

        if dict_data.get("minutes") is not None:
            self.minutes = dict_data["minutes"]
        else:
            self.minutes = {}

    def dump_to_debug(self):
        print("-------------------------------------- Start: Data --------------------------------------------------")

        if len(self.days) > 0:
            print("Day Aggregations")
            print(self.days)

        if len(self.days_hours) > 0:
            print("Day Hours Aggregations")
            print(self.days_hours)

        if len(self.hours) > 0:
            print("Hours Aggregations")
            print(self.hours)

        if len(self.minutes) > 0:
            print("Minutes Aggregations")
            print(self.minutes)

        print("-------------------------------------- End: Data ----------------------------------------------------")

    def get_current_month_numeric_aggregation_from_now(self, aggregate=True, aggregation_key="days"):
        """
        This method will give you data for current month.

        :param aggregation_key:  days, days_hour [currently only days is supported]
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

    def get_last_n_days_numeric_aggregation_from_now(self, days, aggregate=True, aggregation_key="days"):
        """
        :param days: how many days in past (including today)
        :param aggregate:  aggregation or raw values
        :param aggregation_key:  days, days_hour [currently only days is supported]
        :return: if aggregate=True, then single numeric value of the total, otherwise array of values
        """
        return self.get_last_n_days_numeric_aggregation_from_given_time(datetime.now(), days, aggregate,
                                                                        aggregation_key)

    def get_last_n_days_numeric_aggregation_from_given_time(self, time, days, aggregate=True,
                                                            aggregation_key="days"):
        """
        :param time: from ("time") to ("time - n days") -> including today
        :param days: how many days in past (including today)
        :param aggregate:  aggregation or raw values
        :param aggregation_key:  days, days_hour [currently only days is supported]
        :return: if aggregate=True, then single numeric value of the total, otherwise array of values
        """

        # Find the keys
        keys = get_keys_for_n_days_for_day_aggregation(time, days)

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
