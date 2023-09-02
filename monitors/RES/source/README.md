# Ransomware Monitoring

## Prerequisites

- Python 3
- pip (`$ sudo apt install python-pip`)

## Install python dependencies (virtualenv)

```
$ sudo apt install python3-venv
$ python3 -m venv monitor_env
$ source monitor_env/bin/activate
$ pip install -r requirements.txt
```

## Run

`$ python main.py`

## Config

Under `config/config.yaml` is it possible to configure the program.

### General

General settings
A device random id is generated automatically to avoid conflicts, but is it possible to specify a human readable device id.

The final id will become: `deviceId_randomId`

- deviceId: custom device Id (avoid having spaces here)
- csvEnabled: boolean. If the data should be written in a csv file
- logLevel: verbose | debug | log | warn | error
- rabbitMQEnabled: boolean. If the data should be sent via rabbitMQ

Example:

```
general:
  deviceId: sensor_1
  csvEnabled: false
  logLevel: debug
  rabbitMQEnabled: true
```

### Device

- newtork_interface: The device's network interface to monitor.
  Example:

```
device:
  newtork_interface: wlan0
```

### Perf Events

Perf Events to monitor
The events must be available in the device, to see which events can be used simply run `$ perf list` on the device.
A list of events for the device used in the thesis is available [here](docs/perf_events.md)

- perf_events: list of events per category

Example:

```
perf_events:
  cpu: ...
  memory: ...
  network: ...
  io:
    - block:block_rq_complete
    - block:block_rq_insert
    ...
  others: ...
```

### HW Events

Hardware Events to monitor. Please leave this as default

- hw_events: list of events per category

Example:

```
hw_events:
  cpu:
    - cpu
  io:
    - ioread
    - iowrite
    - ioreadbytes
    - iowritebytes
    - ioreadtime
    - iowritetime
    - iobusytime
    - read_merge
    - write_merge
  memory:
    - memory
  network:
    - net_in
    - net_out
    - pkt_in
    - pkt_out
    - err_in
    - err_out
    - drop_in
    - drop_out
```

### Perf

Perf settings

- process: name of the perf process
- monitor_window: time window in seconds that perf will monitor at each iteration (i.e. for how much time perf will monitor the events for every iteration)

Example:

```
perf:
  process: perf_4.9
  monitor_window: 5
```

### RabbitMQ

RabbitMQ config

- host: ip address or hostname of rabbitmq server
- user: rabbitmq username
- password: rabbitmq password
- port: rabbitmq port

```
rabbitMQ:
  host: 127.0.0.1
  user: guest
  password: guest
  port: 5672
```

## Create executable

```
$ pip install pyinstaller
$ pyinstaller --onefile main.py
```
