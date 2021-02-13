import asyncio
import json

from bleak import BleakClient
from bleak import _logger as logger

address = "BC:6A:29:BF:DB:37"
UUID_TX = "0000ffe1-0000-1000-8000-00805f9b34fb"    # HM-10
UUID_RX = "0000ffe1-0000-1000-8000-00805f9b34fb"
my_data = {"hello": "world"}

my_data_ = json.dumps(my_data).encode('utf-8')


def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    print("{0}: {1}".format(sender, data))


async def run(ble_address):
    async with BleakClient(ble_address) as client:
        x = await client.is_connected()
        logger.info("Connected: {0}".format(x))

        await client.write_gatt_char(UUID_TX, bytearray(my_data_))

        await client.start_notify(UUID_RX, notification_handler)
        await asyncio.sleep(5.0)
        await client.stop_notify(UUID_RX)


loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
