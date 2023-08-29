import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import backtrader as bt
import testcommon


class MyStrategy(bt.Strategy):
    params = (
        ("fast_period", 10),
        ("slow_period", 50),
    )

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            self.cancel(order)
        elif order.status in [order.Canceled]:
            print("cancelled order")
        elif order.status in [order.Margin]:
            print("margin order")
        elif order.status in [order.Rejected]:
            print("rejected order")
        elif order.status == order.Completed:
            # Order has been completed
            pass

    def __init__(self):
        self.fast_ma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.fast_period
        )
        self.slow_ma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.slow_period
        )

    def next(self):
        if not self.position:
            buy_price = 5000
            self.buy(exectype=bt.Order.Stop, price=buy_price)
        elif self.fast_ma < self.slow_ma and self.position:
            self.sell()


chkdatas = 1


def test_run(main=False):
    datas = [testcommon.getdata(i) for i in range(chkdatas)]
    testcommon.runtest(
        datas,
        MyStrategy,
        runonce=True,
        preload=True,
        exbar=False,
        plot=main,
    )


if __name__ == "__main__":
    test_run(main=True)
