import unittest

from devlibx_avro_helper.month_data_v1 import MonthDataAvroHelperV1, get_keys_for_current_month_for_day_aggregation, \
    get_keys_for_current_month_for_day_aggregation_from_given_time
from datetime import datetime

# Example time to used in tests
date_time_str_for_this_test = '05/09/22 01:55:19'
date_time_obj_for_this_test = datetime.strptime(date_time_str_for_this_test, '%d/%m/%y %H:%M:%S')


class TestingMonthDataAvroHelperV1(unittest.TestCase):

    def test_string_to_dict_on_input(self):
        input = '''
                {"updated_at":1663665518937,"days":{"9-17":1,"9-4":1,"9-18":1,"9-5":1,"9-15":1,"9-6":1,"9-16":1}}
                '''
        helper = MonthDataAvroHelperV1(input)
        helper.dump_to_debug()

    def test__get_keys_for_current_month_for_day_aggregation_from_given_time(self):
        results = get_keys_for_current_month_for_day_aggregation_from_given_time(date_time_obj_for_this_test)
        print(results)
        self.assertEqual(5, len(results))
        self.assertEqual("9-1", results[0])
        self.assertEqual("9-2", results[1])
        self.assertEqual("9-3", results[2])
        self.assertEqual("9-4", results[3])
        self.assertEqual("9-5", results[4])

    def test__get_keys_for_current_month_for_day_aggregation(self):
        now = datetime.now()
        month = now.month
        day = now.day
        results = get_keys_for_current_month_for_day_aggregation()
        self.assertEqual(day, len(results))
        self.assertEqual("{}-{}".format(month, 1), results[0])
        self.assertEqual("{}-{}".format(month, day), results[-1:][0])

    def test__get_current_month_numeric_aggregation_from_given_time(self):
        # This is the data you will get from DB or some other place
        inputDataFromDB = '''
                      {"updated_at":1663665518937,"days":{"9-1":3,"9-2":1,"9-3":2, "9-4":1, "9-5":1}}
                      '''
        helper = MonthDataAvroHelperV1(inputDataFromDB)

        # Check with aggregate=False
        result = helper.get_current_month_numeric_aggregation_from_given_time(
            date_time_obj_for_this_test,
            aggregate=False
        )
        self.assertEqual(3, result[0])
        self.assertEqual(1, result[1])
        self.assertEqual(2, result[2])
        self.assertEqual(1, result[3])
        self.assertEqual(1, result[4])
        print(result)

        # Check with aggregate=True
        result = helper.get_current_month_numeric_aggregation_from_given_time(date_time_obj_for_this_test)
        print(result)
        self.assertEqual(8, result)

    def test__get_current_month_numeric_aggregation_from_now(self):
        # This is the data you will get from DB or some other place
        inputDataFromDB = '''
                      {"updated_at":1663665518937,"days":{"9-1":3,"9-2":1,"9-3":2, "9-4":1, "9-5":1}}
                      '''
        helper = MonthDataAvroHelperV1(inputDataFromDB)

        # Check with aggregate=False
        result = helper.get_current_month_numeric_aggregation_from_now(aggregate=False)
        self.assertEqual(3, result[0])
        self.assertEqual(1, result[1])
        self.assertEqual(2, result[2])
        self.assertEqual(1, result[3])
        self.assertEqual(1, result[4])
        print(result)

        # Check with aggregate=True
        result = helper.get_current_month_numeric_aggregation_from_now()
        print(result)
        self.assertEqual(8, result)

    def test__get_numeric_aggregation_for_last_n_days_from_given_time(self):
        # This is the data you will get from DB or some other place
        inputDataFromDB = '''
                      {"updated_at":1663665518937,"days":{"9-1":3,"9-2":2,"9-3":7, "9-4":3, "9-5":11}}
                      '''
        helper = MonthDataAvroHelperV1(inputDataFromDB)

        # Check with aggregate=False
        result = helper.get_last_n_days_numeric_aggregation_from_given_time(date_time_obj_for_this_test, 4,
                                                                            aggregate=False)
        print(result)
        self.assertEqual(4, len(result))
        self.assertEqual(11, result[3])
        self.assertEqual(3, result[2])
        self.assertEqual(7, result[1])
        self.assertEqual(2, result[0])
        print(result)

        # Check with aggregate=True
        result = helper.get_last_n_days_numeric_aggregation_from_given_time(date_time_obj_for_this_test, 4)
        print(result)
        self.assertEqual(23, result)

    def test__get_current_month_numeric_aggregation_from_now_for_readme(self):
        # This is the data you will get from DB or some other place
        inputDataFromDB = '''
                      {"updated_at":1663665518937,"days":{"9-1":3,"9-2":1,"9-3":2, "9-4":1, "9-5":1}}
                      '''
        helper = MonthDataAvroHelperV1(inputDataFromDB)

        # Check with aggregate=True
        result = helper.get_current_month_numeric_aggregation_from_now()
        print(result)
        # >> 8

        self.assertEqual(8, result)

    def test__get_last_n_days_numeric_aggregation_from_given_time(self):
        # This is the data you will get from DB or some other place
        inputDataFromDB = '''
                      {"updated_at":1663665518937,"days":{"9-1":3,"9-2":2,"9-3":7, "9-4":3, "9-5":11}}
                      '''
        helper = MonthDataAvroHelperV1(inputDataFromDB)

        # Check with aggregate=True
        result = helper.get_last_n_days_numeric_aggregation_from_given_time(date_time_obj_for_this_test, 4)
        print(result)
        # >> 23
        self.assertEqual(23, result)
