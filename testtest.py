# import asyncio
# import websockets
# import json

# async def process_kline(kline):
#     # Process the kline data here
#     print(f"Processing kline: {kline}")

# async def listen():
#     url = "wss://stream.binance.com/ws/btcusdt@kline_15m@+08:00 "

#     async with websockets.connect(url) as ws:
#         while True:
#             data = await ws.recv()
#             message = json.loads(data)
#             kline = message.get('k', {})
#             await process_kline(kline)

# asyncio.get_event_loop().run_until_complete(listen())


import asyncio
import websockets
import json

async def process_kline(kline):
    # Process the kline data here
    print(f"Processing kline: {kline}")

async def listen():
    # url = "wss://testnet.binance.vision/ws/btcusdt@kline_1m"
    url = "wss://stream.binance.com/ws/btcusdt@kline_15m@+08:00"

    ws = await websockets.connect(url)
    try:
        while True:
            data = await ws.recv()
            message = json.loads(data)
            kline = message.get('k', {})
            await process_kline(kline)
            await asyncio.sleep(1)  # Adjust the sleep duration as needed
    finally:
        await ws.close()

asyncio.run(listen())