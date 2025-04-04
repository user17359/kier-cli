import asyncio

from bleak import BleakClient, BleakError
from rich import print

from kier_cli.movesense_bt.movesense_conncection import MovesenseConnection

disconnect_initiated = False
reconnect_attempts = 5
reconnect_delay = 2

def launch_timed(df, client, units):
    asyncio.create_task(timed_connection(df, client, units))


def launch_stop(client):
    asyncio.create_task(stop_connection(client))


def launch_disconnect(client):
    asyncio.create_task(disconnect_peripheral(client))


async def start_connection(address):
    client = BleakClient(address, disconnected_callback=disconnected_callback)
    try:
        await client.connect()

    except Exception as e:
        print('[red]' + repr(e) + '[red]')
    return client

def disconnected_callback(client):
    global disconnect_initiated
    if not disconnect_initiated:
        print("[red]Device disconnected[/red] ❗")
        asyncio.create_task(reconnect(client))

async def reconnect(client):
    for attempt in range(reconnect_attempts):
        try:
            print(f"Reconnect attempt {attempt + 1}/{reconnect_attempts}")
            await client.connect() 
            await MovesenseConnection().try_connection(client)
            print("[green]Reconnected successfully[/green]")
            break
        except BleakError as e:
            print(f"Reconnection attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(reconnect_delay)
    else:
        print("All reconnection attempts failed")

async def timed_connection(df, client, units):
    await MovesenseConnection().start_connection(df, client, units)


async def stop_connection(client):
    global disconnect_initiated
    disconnect_initiated = True
    await MovesenseConnection().stop_connection(client)
    await disconnect_peripheral(client)


async def disconnect_peripheral(client):
    await client.disconnect()
    print("Disconnected")