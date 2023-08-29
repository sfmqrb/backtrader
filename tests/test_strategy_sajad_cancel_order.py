import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import backtrader as bt


class MyStrategy(bt.Strategy):
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Order has been submitted or accepted, attempt to cancel it
            self.cancel(order)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            # Order has been canceled, margin call, or rejected
            pass

        elif order.status == order.Completed:
            # Order has been completed
            pass

    def next(self):
        # Your strategy logic here
        pass


cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)

# Add data feed and configure cerebro...

# Run the backtest
cerebro.run()
