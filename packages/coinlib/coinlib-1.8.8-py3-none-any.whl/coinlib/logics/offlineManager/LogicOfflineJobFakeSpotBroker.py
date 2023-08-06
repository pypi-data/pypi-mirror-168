import pandas as pd

from coinlib.logics.offlineManager.LogicOfflineJobFakeBroker import LogicOfflineJobFakeBroker, FakeOrder, OrderSide


class LogicOfflineJobFakeSpotBroker(LogicOfflineJobFakeBroker):

    def __init__(self, manager):
        super(LogicOfflineJobFakeSpotBroker, self).__init__(manager)
        pass

    def exchangeOrderAndRemoveAssetValue(self, order: FakeOrder):

        asset = self.manager.getAsset(order.symbol.base)
        if asset is None:
            ## this is an error
            self.onErrorHappenedInBroker("You tried to sell a asset which you dont have. ", order)
        asset.free -= order.quantity
        asset.total -= order.quantity
        portfolio = self.manager.getPortfolio()

        outprice = self.getPrice(symbol=order.symbol.symbol)
        portfolio.getQuoteAsset().free += order.quantity * outprice
        portfolio.getQuoteAsset().total += order.quantity * outprice

        self.manager.updatePortfolio(portfolio)

        return True

    def exchangeOrderAndAddAssetValue(self, order: FakeOrder):
        asset = self.manager.getAsset(order.symbol.base, createIfNotExistant=True)
        asset.free += order.quantity
        asset.total += order.quantity
        if asset.locked > 0:
            asset.locked -= order.quantity

        portfolio = self.manager.getPortfolio()

        portfolio.getQuoteAsset().free -= order.quantity * order.executed_price
        portfolio.getQuoteAsset().total -= order.quantity * order.executed_price

        self.manager.updatePortfolio(portfolio)

        return True

    def onHandleExecutedOrder(self, order: FakeOrder):

        if order.side == OrderSide.SELL:
            self.exchangeOrderAndRemoveAssetValue(order)
        else:
            self.exchangeOrderAndAddAssetValue(order)

