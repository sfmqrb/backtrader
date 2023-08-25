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
    args = {}

    def __init__(self, *args, **kwargs) -> None:
        self.rsi = bt.ind.RSI(self.datas[0], period=14)
        self.ichimoku_sym = bt.ind.Ichimoku(self.datas[0])

        self.inpos = False
        self.exit_buy_signal = True

    def next(self):
        if not self.inpos and self.exit_buy_signal:
            self.sell(size=0.000001)
            self.inpos = True
        elif self.exit_buy_signal:
            self.close()
            self.inpos = False
            self.exit_buy_signal = False


chkdatas = 1


def test_run(main=False):
    datas = [testcommon.getdata(i) for i in range(chkdatas)]
    testcommon.runtest(
        datas,
        TestStrategy,
        runonce=True,
        preload=True,
        exbar=False,
        printdata=main,
        printops=main,
        plot=main,
    )


if __name__ == "__main__":
    test_run(main=True)
