from __future__ import print_function

import grpc
import time

import broker_pb2
import broker_pb2_grpc
import common_pb2
import common_pb2_grpc
  
id = 13
pin = 'gxOu0bVCT'

broker_ip_port = '113.208.112.25:57513'
market_ip_port = '113.208.112.25:57600'
stocks_A = ['A000.PSE', 'A001.PSE', 'A002.PSE']
stocks_B = ['B000.PSE', 'B001.PSE', 'B002.PSE']
'''
Broker
'''
class Broker():
    def __init__(self):
        channel = grpc.insecure_channel(broker_ip_port)
        self.stub = broker_pb2_grpc.BrokerStub(channel)
    
    def Info(self):
        ret = self.stub.info(common_pb2.Empty())
        print(ret)
        return ret

    def Register(self):
        ret = self.stub.register(broker_pb2.RegisterRequest(trader_name = str(id), trader_pin = pin))
        print(ret)
        return ret

    def NewOrder(self, side = 'BID', symbol = stocks_A[0], volume = 1, price = 100, is_market = False, pos_type = 'LONG'):
        ret = self.stub.new_order(broker_pb2.TraderRequest(trader_id = id, trader_pin = pin, 
                            request_type = 'NEW_ORDER', side = side, symbol = symbol, volume = volume,
                            price = price, is_market = is_market, pos_type = pos_type))    
        print('New Order ret:-----------------------------------------------')
        print(ret)
        return ret

    def CancelOrder(self, order_id):
        ret = self.stub.cancel_order(broker_pb2.TraderRequest(trader_id = id, trader_pin = pin, 
                            request_type = 'CANCEL_ORDER', order_id = order_id))
        print(ret)       

    def GetTrader(self, request_type = 'INCREMENTAL_INFO'):
        ret = self.stub.get_trader(broker_pb2.TraderRequest(trader_id = id, trader_pin = pin, 
                            request_type = request_type))   
        print('Get Trader ret:') 
        for rec in ret.market_records:
            print(rec.symbol)
            print(rec.percent)
        print(ret)

'''
Market Data
'''
class Market():
    def __init__(self):
        channel = grpc.insecure_channel(market_ip_port)
        self.stub = broker_pb2_grpc.MarketDataStub(channel)   

    def ListInstruments(self):    
        ret = self.stub.list_instruments(common_pb2.Empty())
        for instrument in ret.instruments:
            print(instrument)

    def Subscribe(self):
        b = Broker()
        #b.Register()
        #b.Info()
        i = 0
        A000 = []
        for response in self.stub.subscribe(common_pb2.Empty()):
            # print(response.instruments)
            i += 1
            if i > 100:
                break
            for ins in response.instruments:
                # print('ok')
                symbol = ins.symbol
                last_price = ins.last_price
                # volume = ins.traded_volume
                # deliver = ins.deliver_price
                if symbol == 'A001.PSE':
                    A000.append(last_price)
                if symbol == 'A000.PSE' or symbol == 'B000.PSE':
                    continue

                # print('================BID {} at price {}'.format(symbol, last_price))
                ret = b.NewOrder(side='BID', symbol=symbol, volume=100, price=last_price-0.01, is_market=False, pos_type='LONG')
                if ret.result_code == 0:
                    ret = b.NewOrder(side='ASK', symbol=symbol, volume=100, price=last_price+0.01, is_market=False, pos_type='LONG')
                # if ret.result_code == 260:
                #     print('BID ' + symbol + ' SHORT ************************************')
                # if ret.result_code == 0:
                #     print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
                #     for rec in ret.market_records:
                #         print(rec.symbol)
                #         print(rec.percent)
                # print('================ASK {} at price {}'.format(symbol, last_price))
                ret = b.NewOrder(side='ASK', symbol=symbol, volume=100, price=last_price-0.01, is_market=False, pos_type='SHORT')
                if ret.result_code == 0:
                    ret = b.NewOrder(side='BID', symbol=symbol, volume=100, price=last_price+0.01, is_market=False, pos_type='SHORT')
                # if ret.result_code == 260:
                #     print('ASK ' + symbol + ' SHORT ************************************')
                # if ret.result_code == 0:
                #     print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
                #     for rec in ret.market_records:
                #         print(rec.symbol)
                #         print(rec.percent)
            # time.sleep(1)
            b.GetTrader()
        return A000

if __name__ == '__main__':
    # b = Broker()   
    # b.Register()
    # b.Info()
    # print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    # b.NewOrder(side = 'BID', symbol=stocks_A[1], volume=100, price=100.1, is_market=True, pos_type='LONG')
    # print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    # b.NewOrder(side = 'ASK', symbol=stocks_A[1], volume=100, price=100.1, is_market=True, pos_type='SHORT')
    # while(True):
    #     for j in range(10):
    #         for i in range(1, 3):
    #             a = b.NewOrder(side = 'BID', symbol = stocks_A[i], volume=100, price=100.1, is_market=True, pos_type='LONG')
    #             c = b.NewOrder(side = 'ASK', symbol = stocks_A[i], volume=100, price=99.9, is_market=True, pos_type='SHORT')
    #     time.sleep(1)
    # b.GetTrader()
    # 
    # orders = []
    # for order in a.orders.orders:
    #     orders.append(order)
    # print(orders[0])
    # b.CancelOrder(orders[0])
    # b.GetTrader()

    m = Market()
    m.ListInstruments()
    x = m.Subscribe()
    print(x)
    
