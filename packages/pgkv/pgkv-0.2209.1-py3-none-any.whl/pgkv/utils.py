#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time


def get_timestamp_ms() -> int:
    return int(round(time.time() * 1000))
