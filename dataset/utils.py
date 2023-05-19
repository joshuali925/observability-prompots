import datetime
import random
import time

mintime_ts = int(time.mktime(datetime.datetime(2022, 8, 6, 8, 14, 59).timetuple()))
maxtime_ts = int(time.mktime(datetime.datetime(2023, 5, 19, 20, 14, 59).timetuple()))


def rand_time():
    random_ts = random.randint(mintime_ts, maxtime_ts)
    return datetime.datetime.fromtimestamp(random_ts)
