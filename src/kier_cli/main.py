import time
import pickle
import asyncio
import csv

from rich import print
from rich.progress import track

import typer

from kier_cli.movesense_bt.timed_conncection import start_connection, stop_connection, timed_connection


app = typer.Typer()

def load_sensors():
    try:
        dbfile = open('pickledList', 'rb')    
        return pickle.load(dbfile)
    except:
        return []

@app.command()
def add(name: str, mac: str):
    list_sensors = load_sensors()

    if any(d['name'] == name for d in list_sensors):
        print("[red]Name already taken! 🚫[/red]")
        return

    list_sensors.append({"name": name, "mac": mac})
    dbfile = open('pickledList', 'wb')
    pickle.dump(list_sensors, dbfile)                    
    dbfile.close()

    print(f"Registered sensor [bold blue]{name}[/bold blue] at MAC address {mac}")

@app.command()
def forget(name: str):
    list_sensors = load_sensors()

    if not any(d['name'] == name for d in list_sensors):
        print("[red]No such sensor registered! 🚫[/red]")
        return

    list_sensors = [d for d in list_sensors if d.get('name') != name]
    dbfile = open('pickledList', 'wb')
    pickle.dump(list_sensors, dbfile)                    
    dbfile.close()

    print(f"Deregistered sensor [bold blue]{name}[/bold blue]")

@app.command()
def list():
    list_sensors = load_sensors()
    print("List of registered sensors 📡:")
    for sensor in list_sensors:
        print(f'[bold blue]{sensor["name"]}[/bold blue] {sensor["mac"]}')

async def _measure(name: str, duration: int):
    print(f"Start of measurement for [bold blue]{name}[/bold blue]")

    list_sensors = load_sensors()

    if not any(d['name'] == name for d in list_sensors):
        print("[red]No such sensor! 🚫[/red]")
        return
    else:
        mac = next(d for d in list_sensors if d["name"] == name)["mac"]
    
        client = await start_connection(mac)
        data_storage = {"ecg":[]}
        
        await timed_connection(
                units=[{"name": "ecg", "probing": "250"}],
                df=data_storage,
                client=client)

        total = 0
        for value in track(range(duration), description="Measuring 📡 "):
            await asyncio.sleep(1)
            total += 1

        await stop_connection(client)

        print(len(data_storage["ecg"]))

        # Get first of ecg - modify if not only for ECG
        csv_file = 'data' + str(data_storage["ecg"][0][0]) + '.csv'

        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)

            for data_type, values in data_storage.items():
                writer.writerow([data_type, "Timestamp", "Value"])

                for value in values:
                    writer.writerow([data_type, value[0], value[1]])

                writer.writerow([])

        
        
        print(f"Saved measurement from [bold blue]{name}[/bold blue] to file [blue]{csv_file}[/blue] 💾")

@app.command()
def measure(name: str, duration: int):
    asyncio.run(_measure(name, duration))


if __name__ == "__main__":
    app()
