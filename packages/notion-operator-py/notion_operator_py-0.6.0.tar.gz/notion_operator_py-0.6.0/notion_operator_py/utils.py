# -*- coding: utf-8 -*-
# @Filename : utils
# @Date : 2022-07-25-13-30
# @Project: nt-integration-sdk

import datetime


def iso8601_date(year=2022, month=1, day=1, hours=00, minutes=00, seconds=00, include_time: bool = False):
    dt = datetime.datetime(int(year), int(month), int(day), int(hours), int(minutes), int(seconds), 000000)
    if include_time:
        formatter = "%Y-%m-%dT%H:%M:%SZ"
    else:
        formatter = "%Y-%m-%d"

    return dt.strftime(formatter)
