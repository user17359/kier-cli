import time
import pickle

from rich import print
from rich.progress import track

import typer

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
        print(f"[bold blue]{sensor["name"]}[/bold blue] {sensor["mac"]}")

@app.command()
def measure(name: str, duration: int):
    print(f"Start of measurement for [bold blue]{name}[/bold blue]")
    total = 0
    for value in track(range(duration), description="Measuring 📡 "):
        time.sleep(1)
        total += 1
    print(f"Saved measurement from [bold blue]{name}[/bold blue] to file [blue]data.csv[/blue] 💾")

if __name__ == "__main__":
    app()