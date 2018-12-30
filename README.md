# PMS5003-Python

The [PM2.5 Air Quality Sensor](https://learn.adafruit.com/pm25-air-quality-sensor) allows for real-time monitoring of PM10, PM2.5 and PM10.0 concentrations. 

To use it with a Raspberry PI, the TXD and RXD ports must be connected to the RX and TX serial ports in the RPI, respectively. In Raspbian, the serial port is assigned to the Linux console by default. To disable this behavior, use the [raspi-config](https://www.raspberrypi.org/documentation/configuration/raspi-config.md) utility. 

```
sudo raspi-config
```
Once the blue screen appears, go to `Interfacing options`, and then to `Serial`. Here you select No.  

A copy of the datasheet of the PM2.5 Air Quality Sensor can be found [here](https://cdn-shop.adafruit.com/product-files/3686/plantower-pms5003-manual_v2-3.pdf).
