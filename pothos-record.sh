#!/bin/sh
if [ ! -d "$HOME/sdr-ble-demo" ]; then
  mkdir -pv ~/sdr-ble-demo
  git clone https://github.com/DesignSparkrs/sdr-ble-demo/ ~/sdr-ble-demo
fi

PothosFlow ~//btle_printer_float32.pth 2>&1 | grep "Address" | cut -f4- -d' ' | sed 's!\\!\\\\\\\\!g' | sed 's/\x1b\[[0-9;]*m//g' > /tmp/fifo1
