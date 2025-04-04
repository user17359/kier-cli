# kier-cli ❤️

The package provides simple CLI client for collecting Movesense sensor data.

## Supported sensor firmware
The firmware required to connect with this client can be collected from:
https://github.com/JonasPrimbs/movesense-ble-ecg-firmware

## Installation

To install kier-cli, follow these steps:
1. **Download latest release**
You can download the latest release from the [releases page](https://github.com/user17359/kier-cli/releases)
2. **Create a venv and activate it**
```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. **Install the package**
```sh
pip install [file-name]
```
4. **Check if the installation was proper**
```sh
kier-cli --help
```

## Usage

App maintains list of sensors for measurement, to add a sensor use:
```sh
kier-cli add [name] [mac-address]
```

To remove previosuly added one:
```sh
kier-cli forget [name]
```

To display the list:
```sh
kier-cli list
```

And to perform a measurement
```sh
kier-cli measure [name] [duration]
```
