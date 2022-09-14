from ib_insync import *
import datetime
import time

import nest_asyncio
nest_asyncio.apply()

# util.startLoop()  # uncomment this line when in a notebook
clid = 1

ib = IB()

def onErrorEvent( reqId, errorCode, errorString, contract):
    
    if "has been restored" in errorString:
        print(reqId, errorCode, errorString, contract)
        raise KeyboardInterrupt


if __name__ == '__main__':

    ib.errorEvent += onErrorEvent

    ib.connect('127.0.0.1', 7497, clientId=clid)

    ib.reqMarketDataType(3)

    contracts = [Forex(pair) for pair in ('EURUSD', 'GBPUSD')]
    ib.qualifyContracts(*contracts)

    eurusd = contracts[0]
    gbpusd = contracts[1]

    while True:
        try:
            if ib.isConnected() == False:
                clid = clid + 1
                print("...attempting to reconnect to TWS")
                ib.connect('127.0.0.1', 7497, clientId=clid)
                ib.reqMarketDataType(3)

            for contract in contracts:
                ib.reqMktData(contract, '', False, False)


            ticker = ib.ticker(eurusd)
            ib.sleep(2)
            print(ticker)
            print("EURUSD marketPrice", ticker.marketPrice())

            ticker = ib.ticker(gbpusd)
            ib.sleep(2)
            print(ticker)
            print("GBPUSD marketPrice", ticker.marketPrice())

            #print("Loop that prints ticker.marketPrice()")
            for i in range(2):
                time.sleep(2)
                print(ticker.time.astimezone(), "- GBPUSD marketPrice is", ticker.marketPrice())

            start = ''
            end = datetime.datetime.now()
            ticks = ib.reqHistoricalTicks(eurusd, start, end, 1000, 'BID_ASK', useRth=True)

            print(ticks[-1])
        except:
            ib.disconnect()
            time.sleep(3)

    ib.disconnect()
