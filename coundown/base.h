#ifndef BASE
  #define BASE

#include <stdint.h>
#include <Arduino.h>

#define EEPROM_ADDR 0b10100000 
#define RTC_ADDR 0b11010000

#define ACK 1
#define NACK 0

namespace i2c
{
  void start();

  void stop();

  uint8_t addr(uint8_t addr_rw);

  void write(uint8_t data);

  uint8_t read(uint8_t ack);
}

namespace eeprom
{
  void write(unsigned short addr, uint8_t data);

  uint8_t read(unsigned short addr);

  void writeShort(uint16_t addr, uint16_t data);

  uint16_t readShort(uint16_t addr);

  void readExternal(uint16_t addr, uint8_t size, uint8_t *buffer);
}

#endif