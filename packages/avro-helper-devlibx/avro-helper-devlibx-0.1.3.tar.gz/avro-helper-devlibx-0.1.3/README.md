### How to use

Install ```pip install avro-helper-devlibx```

# Quick example - V1

### Debug what data I have

```python
from devlibx_avro_helper.month_data_v1 import MonthDataAvroHelperV1

input = '''{"updated_at":1663665518937,"days":{"9-17":1,"9-4":1,"9-18":1,"9-5":1,"9-15":1,"9-6":1,"9-16":1}}'''
helper = MonthDataAvroHelperV1(input)
helper.dump_to_debug()

# Print the data
# -------------------------------------- Start: Data --------------------------------------------------
# Day Aggregations
# {'9-17': 1, '9-4': 1, '9-18': 1, '9-5': 1, '9-15': 1, '9-6': 1, '9-16': 1}
# -------------------------------------- End: Data ----------------------------------------------------
```

### Get data for this month (from today to start of this month)

```python
from devlibx_avro_helper.month_data_v1 import MonthDataAvroHelperV1


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
```

### Get data for last N days (from today to last n days - including today)

```python
from devlibx_avro_helper.month_data_v1 import MonthDataAvroHelperV1
from datetime import datetime


def test__get_last_n_days_numeric_aggregation_from_given_time(self):
    # This is the data you will get from DB or some other place
    inputDataFromDB = '''
                      {"updated_at":1663665518937,"days":{"9-1":3,"9-2":2,"9-3":7, "9-4":3, "9-5":11}}
                      '''
    helper = MonthDataAvroHelperV1(inputDataFromDB)

    # Check with aggregate=True
    result = helper.get_last_n_days_numeric_aggregation_from_given_time(datetime.now(), 4)
    print(result)
    # >> 23
    self.assertEqual(23, result)
```

---

#### Quick example

```python
from devlibx_avro_helper.month_data import MonthDataAvroHelper

base64Str = "BgY3LTMCBjYtNgIGNy01BAAAAAI="
helper = MonthDataAvroHelper()
result = helper.process(base64Str)
print(result)

# Result
# {'days': {'8-16': 110, '8-17': 111, '8-14': 108, '8-15': 109, '8-18': 112, '8-19': 113, '8-30': 124, '8-31': 125, '8-12': 106, '8-13': 107, '8-10': 104, '8-11': 105, '9-1': 126, '9-2': 127, '9-3': 128, '8-27': 121, '9-4': 129, '8-6': 100, '8-28': 122, '8-7': 101, '8-25': 119, '8-8': 102, '8-26': 120, '8-9': 103, '8-29': 123, '8-20': 114, '8-23': 117, '8-24': 118, '8-21': 115, '8-22': 116}, 'entity_id': 'harish_1'}
```

### Get data for this month

In this example we would have data in base 64 encoding. We will get aggregated data for this month

```python
from devlibx_avro_helper.month_data import MonthDataAvroHelper
from datetime import datetime


def test_process_and_return_aggregation_for_month(self):
    base64Str = "AgoGNy0xAgY3LTICBjctMwIGNy00AgY3LTUKAAAAAAI="
    helper = MonthDataAvroHelper()
    result = helper.process(base64Str)
    print(result)
    # Output = {'days': {'7-1': 1, '7-2': 1, '7-3': 1, '7-4': 1, '7-5': 5}, 'days_str': None, 'entity_id': None, 'sub_entity_id': None, 'version': 1}

    date_time_str = '05/07/22 01:55:19'
    date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

    # if you are looking for data for this month then use can use
    # helper.process_and_return_aggregation_for_this_month(base64Str)
    result = helper.process_and_return_aggregation_for_month(date_time_obj, base64Str)
    self.assertEqual(9, result, "result should be 9")
    # Output = 9
```

### Get data for this week (last 7 days)

```python
from devlibx_avro_helper.month_data import MonthDataAvroHelper
from datetime import datetime


def test_process_and_return_aggregation_for_week(self):
    # Test 1 - data from generateDataFor_test_parsing_Test_2
    base64Str = "Ag4INi0yOQIGNy0xAgY3LTICCDYtMzACBjctMwIGNy00AgY3LTUKAAAAAAI=="
    helper = MonthDataAvroHelper()
    result = helper.process(base64Str)
    print(result)
    # Output = {'days': {'6-29': 1, '7-1': 1, '7-2': 1, '6-30': 1, '7-3': 1, '7-4': 1, '7-5': 5}, 'days_str': None, 'entity_id': None, 'sub_entity_id': None, 'version': 1}

    date_time_str = '05/07/22 01:55:19'
    date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

    # if you are looking for data for this month then use can use
    # helper.process_and_return_aggregation_for_this_week(base64Str)
    result = helper.process_and_return_aggregation_for_week(date_time_obj, base64Str)
    self.assertEqual(11, result, "result should be 9")
    # Output = 11
```

### Get data for day

```python
from devlibx_avro_helper.month_data import MonthDataAvroHelper
from datetime import datetime


def test_process_and_return_for_day(self):
    # Test 1 - data from generateDataFor_test_parsing_Test_2
    base64Str = "Ag4INi0yOQIGNy0xAgY3LTICCDYtMzACBjctMwIGNy00AgY3LTUKAAAAAAI=="
    helper = MonthDataAvroHelper()
    result = helper.process(base64Str)
    print(result)
    # Output = {'days': {'6-29': 1, '7-1': 1, '7-2': 1, '6-30': 1, '7-3': 1, '7-4': 1, '7-5': 5}, 'days_str': None, 'entity_id': None, 'sub_entity_id': None, 'version': 1}

    date_time_str = '05/07/22 01:55:19'
    date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

    # if you are looking for data for this month then use can use
    # helper.process_and_return_aggregation_for_this_month(base64Str)
    result = helper.process_and_return_for_today(date_time_obj, base64Str)
    self.assertEqual(5, result, "result should be 9")
    # Output = 5
```

### Get string data for this month

```python
from devlibx_avro_helper.month_data import MonthDataAvroHelper
from datetime import datetime


def test_process_and_return_string_data_for_month(self):
    # Test 1 - data from generateDataFor_test_parsing_Test_2
    base64Str = "AAIOCDYtMjkCAgKamZmZmZnxPwAAAg5tLTE7bS0zAAAAAAAGNy0xAgYCMzMzMzMzC0AAAAIWbS0zO20tNDttLTYAAAAAAAY3LTICCALNzMzMzMwQQAAAAhZtLTQ7bS03O20tOAAAAAAACDYtMzACBAJmZmZmZmYCQAAAAhhtLTI7bS0xO20tMTEAAAAAAAY3LTMCCgJmZmZmZmYWQAAAAhZtLTM7bS02O20tOAAAAAAABjctNAIMAjMzMzMzMx9AAAACGG0tMjttLTc7bS0xMAAAAAAABjctNQIOAs3MzMzMzCFAAAACIG0tMjttLTU7bS03O20tMTAAAAAAAAAC"
    helper = MonthDataAvroHelper()
    result = helper.process(base64Str)
    print(result)
    # Output = {'ParentContainer': [], 'data': {'6-29': {'counter': 1, 'aggregate': 1.1, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-3', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-1': {'counter': 3, 'aggregate': 3.4, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-3;m-4;m-6', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-2': {'counter': 4, 'aggregate': 4.2, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-4;m-7;m-8', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '6-30': {'counter': 2, 'aggregate': 2.3, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-2;m-1', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-3': {'counter': 5, 'aggregate': 5.6, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-3;m-6;m-8', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-4': {'counter': 6, 'aggregate': 7.8, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-2;m-7;m-10', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-5': {'counter': 7, 'aggregate': 8.9, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-2;m-5;m-7;m-10', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}}, 'version': 1}

    date_time_str = '05/07/22 01:55:19'
    date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

    # if you are looking for data for this month then use can use
    # helper.process_and_return_aggregation_for_this_month(base64Str)
    result = helper.process_and_return_string_data_for_month(date_time_obj, base64Str)
    self.assertEqual(8, result, "result should be 8")
    # Output = 8

    date_time_str = '30/06/22 01:55:19'
    date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

    result = helper.process_and_return_string_data_for_month(date_time_obj, base64Str)
    self.assertEqual(4, result, "result should be 4")
    # Output = 8
```

### Get string data for this week

```python
from devlibx_avro_helper.month_data import MonthDataAvroHelper
from datetime import datetime


def test_process_and_return_string_data_for_week(self):
    # Test 1 - data from generateDataFor_test_parsing_Test_2
    base64Str = "AAIOCDYtMjkCAgKamZmZmZnxPwAAAg5tLTE7bS0zAAAAAAAGNy0xAgYCMzMzMzMzC0AAAAIWbS0zO20tNDttLTYAAAAAAAY3LTICCALNzMzMzMwQQAAAAhZtLTQ7bS03O20tOAAAAAAACDYtMzACBAJmZmZmZmYCQAAAAhhtLTI7bS0xO20tMTEAAAAAAAY3LTMCCgJmZmZmZmYWQAAAAhZtLTM7bS02O20tOAAAAAAABjctNAIMAjMzMzMzMx9AAAACGG0tMjttLTc7bS0xMAAAAAAABjctNQIOAs3MzMzMzCFAAAACIG0tMjttLTU7bS03O20tMTAAAAAAAAAC"
    helper = MonthDataAvroHelper()
    result = helper.process(base64Str)
    print(result)
    # Output = {'ParentContainer': [], 'data': {'6-29': {'counter': 1, 'aggregate': 1.1, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-3', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-1': {'counter': 3, 'aggregate': 3.4, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-3;m-4;m-6', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-2': {'counter': 4, 'aggregate': 4.2, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-4;m-7;m-8', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '6-30': {'counter': 2, 'aggregate': 2.3, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-2;m-1', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-3': {'counter': 5, 'aggregate': 5.6, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-3;m-6;m-8', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-4': {'counter': 6, 'aggregate': 7.8, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-2;m-7;m-10', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-5': {'counter': 7, 'aggregate': 8.9, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-2;m-5;m-7;m-10', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}}, 'version': 1}

    date_time_str = '05/07/22 01:55:19'
    date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

    # if you are looking for data for this month then use can use
    # helper.process_and_return_aggregation_for_this_month(base64Str)
    result = helper.process_and_return_string_data_for_week(date_time_obj, base64Str)
    print(result)
    self.assertEqual(10, result, "result should be 10")
    # Output = 10
```

### Get string data for the day

```python
from devlibx_avro_helper.month_data import MonthDataAvroHelper
from datetime import datetime


def test_process_and_return_string_data_for_day(self):
    # Test 1 - data from generateDataFor_test_parsing_Test_2
    base64Str = "AAIOCDYtMjkCAgKamZmZmZnxPwAAAg5tLTE7bS0zAAAAAAAGNy0xAgYCMzMzMzMzC0AAAAIWbS0zO20tNDttLTYAAAAAAAY3LTICCALNzMzMzMwQQAAAAhZtLTQ7bS03O20tOAAAAAAACDYtMzACBAJmZmZmZmYCQAAAAhhtLTI7bS0xO20tMTEAAAAAAAY3LTMCCgJmZmZmZmYWQAAAAhZtLTM7bS02O20tOAAAAAAABjctNAIMAjMzMzMzMx9AAAACGG0tMjttLTc7bS0xMAAAAAAABjctNQIOAs3MzMzMzCFAAAACIG0tMjttLTU7bS03O20tMTAAAAAAAAAC"
    helper = MonthDataAvroHelper()
    result = helper.process(base64Str)
    print(result)
    # Output = {'ParentContainer': [], 'data': {'6-29': {'counter': 1, 'aggregate': 1.1, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-3', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-1': {'counter': 3, 'aggregate': 3.4, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-3;m-4;m-6', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-2': {'counter': 4, 'aggregate': 4.2, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-4;m-7;m-8', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '6-30': {'counter': 2, 'aggregate': 2.3, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-2;m-1', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-3': {'counter': 5, 'aggregate': 5.6, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-3;m-6;m-8', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-4': {'counter': 6, 'aggregate': 7.8, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-2;m-7;m-10', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-5': {'counter': 7, 'aggregate': 8.9, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-2;m-5;m-7;m-10', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}}, 'version': 1}

    date_time_str = '05/07/22 01:55:19'
    date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

    # if you are looking for data for this month then use can use
    # helper.process_and_return_aggregation_for_this_month(base64Str)
    result = helper.process_and_return_string_data_for_day(date_time_obj, base64Str)
    self.assertEqual(4, result, "result should be 4")
    # Output = 4
```