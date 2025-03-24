import time

from rich import print
from rich.progress import track

import typer

app = typer.Typer()


@app.command()
def add(name: str, mac: str):
    print(f"Registered sensor [bold blue]{name}[/bold blue] at MAC address {mac}")

@app.command()
def forget(name: str):
    print(f"Deregistered sensor [bold blue]{name}[/bold blue]")

@app.command()
def list():
    print("List of registered sensors:")

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