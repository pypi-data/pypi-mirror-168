EZX API
===============
EZX Api Network Client, messages and library functions for sending and receiving orders to the EZX iServer.

Installing
==========

```bash

    pip install ezx-pyapi
    
```

Usage
=====

The iServer API is not really designed to be run interactively, although it is possible to do it, as shown below. 
The easiest way to familiarize yourself with the API is to download and run the sample API app, [ezx-sample-py](https://github.com/EZXInc/ezx-sample-py), from Github.

```python

	import logging
	FORMAT='%(asctime)s %(levelname)s: Thread-%(thread)d %(name)s %(funcName)s  %(message)s'
	logging.basicConfig(level=logging.INFO,format=FORMAT,stream=sys.stdout,force=True)
	from iserver.net import ConnectionInfo,ApiClient
	info = ConnectionInfo(host='192.168.1.218',company='FEIS',user='igor',password='igor', port=15000)
	client=ApiClient(info)
	client.start()
	
	# send an order
	from iserver.msgs.convenience_msgs import NewOrder
	order = NewOrder('ZVZZT',1,100,1.25,'SIMU')
	client.send_message(order)
	
```

The default message handler just prints the responses from the server.  You can set your own handler as follows:

```python

	from iserver.msgs.OrderResponse import OrderResponse
	
	responses = []
	import iserver.net
	def my_msg_handler(msg_subtype: int, msg: EzxMsg):
		iserver.net.empty_msg_handler(msg_subtype, msg) # print the message
		# write your handling logic here.
		responses.append(msg)
		
	client._msg_handler = my_msg_handler  # normally this is set in the ApiClient constructor
	
	client.send_message(order)
			
```

Also see the [EZX API Quick Start Guide](https://docs.google.com/document/d/1VcAYjFDZfIbQCVmVN4CZ_U6d3O3dHbnFNuiIBec8L3M) for more details on the API.



	

    