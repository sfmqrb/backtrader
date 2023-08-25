#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2015-2023 Daniel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from __future__ import absolute_import, division, print_function, unicode_literals

import time

try:
    time_clock = time.process_time
except:
    time_clock = time.clock

import testcommon

import backtrader as bt


class TestStrategy(bt.Strategy):
    def __init__(self, params=None) -> None:
        self.watched_order_statuses = ["margin"]
        self.order = None
        self.first_time = True

    def should_trade(self):
        return self.datetime.date().day >= 15 or self.datetime.date().day <= 2

    def notify_order(self, order: bt.Order):
        print("order status", order.status)
        print("day of month", self.datetime.date().day)
        if not self.should_trade():
            if order and order.status in [bt.Order.Submitted, bt.Order.Accepted]:
                print("fucking here")
                self.cancel(order)

    def next(self):
        if self.position:
            print("SELL CREATE, %.2f" % self.data.close[0])
            self.sell()
        elif self.first_time:
            price = 3000
            print("order set")
            self.buy(exectype=bt.Order.Stop, price=price)
            self.first_time = False


chkdatas = 1


def test_run(main=False):
    datas = [testcommon.getdata(i) for i in range(chkdatas)]
    testcommon.runtest(
        datas,
        TestStrategy,
        runonce=True,
        preload=True,
        exbar=False,
        plot=main,
    )


if __name__ == "__main__":
    test_run(main=True)
