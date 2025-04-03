import asyncio

from bleak import BleakClient
from rich import print

from movesense_bt.movesense_conncection import MovesenseConnection

def launch_timed(df, client, units):
    asyncio.create_task(timed_connection(df, client, units))


def launch_stop(client):
    asyncio.create_task(stop_connection(client))


def launch_disconnect(client):
    asyncio.create_task(disconnect_peripheral(client))


async def start_connection(address):
    client = BleakClient(address)
    try:
        await client.connect()

    except Exception as e:
        print('[red]' + repr(e) + '[red]')
    return client


async def timed_connection(df, client, units):
    await MovesenseConnection().start_connection(df, client, units)


async def stop_connection(client):
    await MovesenseConnection().stop_connection(client)
    await disconnect_peripheral(client)


async def disconnect_peripheral(client):
    await client.disconnect()
    print("Disconnected")