# python_rfid

## Description

This library implements an interface to communicate with RFID cards through an MFRC522 device. In spite of other MFRC522 libraries, this project does not depend on particular GPIO libraries written for any particular board, but instead builds upon the Linux kernel's gpio device implementation. In the same spirit, it also avoids dependance on any particular SPI implementation but uses the spidev package, which in turn depends on the Linux SPI userspace API.

## Contributions

Most of the code in this project is based on on the arduino library for the MFRC522 by miguelbalboa, although it has been very heavily restructured to make better use of object oriented design. The original code and *un*license can be found at [https://github.com/miguelbalboa/rfid].