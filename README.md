# fix-ib-api-reconnect
Ensure that ib-insync bot is reconnected automatically

The script test-tickdata.py is an example script that continuously gets tick-data from IB TWS.
A disconnection event can happen in two ways: 
- it can be because TWS has been closed 
- or network connection is lost
The desired behavior is that an ib_insync script can automatically re-establish the connection after TWS or network comes back.

A suggestion from IB_INSYNC forum:
'''
https://github.com/erdewit/ib_insync/issues/469
ib = IB()
ib.disconnectedEvent += lambda: asyncio.create_task(reconnect())
'''

However In the current solution we try to solve both TWS restart and connection loss in a stable way. 
- Exception handling performs a disconnection and reconnection using the ib library function.
- The callback of ib.errorEvent is more tricky: it raises a KeyboardInterrupt event to force the script to "wake up" because it seems that some kind of bug blocks IB's functions to continue after a network loss connection
