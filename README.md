# PMS5003-Python

The [PM2.5 Air Quality Sensor](https://learn.adafruit.com/pm25-air-quality-sensor) allows for real-time monitoring of PM10, PM2.5 and PM10.0 concentrations. 

To use it with a Raspberry PI, the TXD and RXD ports must be connected to the RX and TX serial ports in the RPI, respectively. In Raspbian, the serial port is assigned to the Linux console by default. To disable this behavior, use the [raspi-config](https://www.raspberrypi.org/documentation/configuration/raspi-config.md) utility. 

```
$ sudo raspi-config
```
Once the blue screen appears, go to `Interfacing options`, and then to `Serial`. Here you select `No`.  

A copy of the datasheet of the PM2.5 Air Quality Sensor can be found [here](https://cdn-shop.adafruit.com/product-files/3686/plantower-pms5003-manual_v2-3.pdf).


In addition to the Python 3 packages included in Raspbian Stretch, the `pms500` requires the `pyserial` and `pyyaml` packages. To install them, please run:

```
$ pip3 install -r requirements.txt
```

To execute the example, simply run:

```
$ sudo ./air_quality.py
{'PM1_std': 14, 'PM1_env': 14, 'P5': 0, 'P25': 2, 'P05': 709, 'PM25_std': 17, 'P1': 68, 'PM10_std': 17, 'PM25_env': 17, 'P10': 0, 'P03': 2436, 'PM10_env': 17}
{'PM1_std': 14, 'PM1_env': 14, 'P5': 0, 'P25': 2, 'P05': 749, 'PM25_std': 18, 'P1': 79, 'PM10_std': 18, 'PM25_env': 18, 'P10': 0, 'P03': 2553, 'PM10_env': 18}
{'PM1_std': 16, 'PM1_env': 16, 'P5': 0, 'P25': 2, 'P05': 803, 'PM25_std': 20, 'P1': 90, 'PM10_std': 20, 'PM25_env': 20, 'P10': 0, 'P03': 2679, 'PM10_env': 20}
^C
Terminating data collection
```
