import dateparser
import time


# returns epoch seconds!
def string_to_epoch(date_str=None, time_str=None):
    return dateparser.parse(date_str + ' ' + time_str, settings={'TIMEZONE': 'US/Pacific'}).strftime('%s')