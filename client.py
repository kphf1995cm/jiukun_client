from __future__ import print_function

import grpc
import time

import broker_pb2
import broker_pb2_grpc
import common_pb2
import common_pb2_grpc

id = 13
pin = 'gxOu0bVCT'
broker_ip_port = '113.208.112.25:57501'
#new_broker_ip_port='113.208.112.25:57501'
#new_trader_id = 3
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
        print("---------------info--------------------------")
        print(ret)
        print("---------------------------------------------")
        return ret

    def Register(self):
        ret = self.stub.register(broker_pb2.RegisterRequest(trader_name = str(id), trader_pin = pin))
        print("---------------register-----------------------")
        print(ret)
        print("----------------------------------------------")
        return ret

    def NewOrder(self, side = 'BID', symbol = stocks_A[0], volume = 1, price = 100, is_market = False, pos_type = 'LONG'):
        ret = self.stub.new_order(broker_pb2.TraderRequest(trader_id = id, trader_pin = pin, 
                            request_type = 'NEW_ORDER', side = side, symbol = symbol, volume = volume,
                            price = price, is_market = is_market, pos_type = pos_type))    
        print('----------------NewOrder---------------------')
        print(ret)
        print('---------------------------------------------')
        return ret

    def CancelOrder(self, order_id):
        ret = self.stub.cancel_order(broker_pb2.TraderRequest(trader_id = id, trader_pin = pin, 
                            request_type = 'CANCEL_ORDER', order_id = order_id))
        print('---------------CancelOrder-------------------')
        print(ret)       
        print('---------------------------------------------')

    def GetTrader(self, request_type = 'INCREMENTAL_INFO'):
        ret = self.stub.get_trader(broker_pb2.TraderRequest(trader_id = id, trader_pin = pin, 
                            request_type = request_type))   
        print('--------------GetTrader-----------------------') 
        #print(ret)
        for rec in ret.market_records:
            print(rec.symbol)
            print(rec.percent)
        print('----------------------------------------------')

'''
Market Data
'''
class Market():
    def __init__(self):
        channel = grpc.insecure_channel(market_ip_port)
        self.stub = broker_pb2_grpc.MarketDataStub(channel)   

    def ListInstruments(self):    
        ret = self.stub.list_instruments(common_pb2.Empty())
        print('-----------------ListInstruments-------------')
        for instrument in ret.instruments:
            print(instrument)
        print('---------------------------------------------')

    def Subscribe(self):
        print('-----------------Subscribe-----------------------')
        for response in self.stub.subscribe(common_pb2.Empty()):
            print(response)
        print('-------------------------------------------------')

if __name__ == '__main__':
    b = Broker()   
    b.Register()
    b.Info()
    '''
    for j in range(100):
        for i in range(1, 3):
            a = b.NewOrder(side = 'BID', symbol = stocks_A[i], volume=100, price=99.99, is_market=True, pos_type='LONG')
            c = b.NewOrder(side = 'ASK', symbol = stocks_A[i], volume=100, price=100.01, is_market=True, pos_type='SHORT')
    '''
    b.GetTrader('FULL_INFO')
    #b.GetTrader('INCREMENTAL_INFO')
    
    # orders = []
    # for order in a.orders.orders:
    #     orders.append(order)
    # print(orders[0])
    # b.CancelOrder(orders[0])
    # b.GetTrader()

    #m = Market()
    #m.ListInstruments()
    #m.Subscribe()
    
