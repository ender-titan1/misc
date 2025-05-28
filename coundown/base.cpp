#include "base.h"

namespace i2c
{

  void start() 
  {
    TWCR = (1<<TWINT) | (1<<TWEN) | (1<<TWSTA);
    while (!(TWCR & (1<<TWINT)));
  }

  void stop() 
  {
    TWCR = (1<<TWINT) | (1<<TWEN) | (1<<TWSTO);
    while (!(TWCR & (1<<TWSTO)));
  }

  uint8_t addr(uint8_t addr_rw) 
  {
    TWDR = addr_rw;
    TWCR = (1<<TWINT) | (1<<TWEN);
    while (!(TWCR & (1<<TWINT)));

    return (TWSR & 0xF8);
  }

  void write(uint8_t data) 
  {
    TWDR = data;
    TWCR = (1<<TWINT) | (1<<TWEN);
    while (!(TWCR & (1<<TWINT)));
  }

  uint8_t read(uint8_t ack) 
  {
    TWCR = (1<<TWINT) | (ack<<TWEA) | (1<<TWEN);
    while (!(TWCR & (1<<TWINT)));
    return TWDR;
  }
}

namespace eeprom {
  void write(unsigned short addr, uint8_t data)
  {
    while(EECR & (1<<EEPE)); // Wait until previous write finished

    EEAR = addr;
    EEDR = data;

    // Begin write
    EECR |= (1<<EEMPE);
    EECR |= (1<<EEPE);
  }

  uint8_t read(unsigned short addr)
  {
    while(EECR & (1<<EEPE)); // Wait until previous write finished
    EEAR = addr;

    // Begin read
    EECR |= (1<<EERE);
    return EEDR;
  }

  void writeShort(uint16_t addr, uint16_t data)
  {
    write(addr, data >> 8);        // Write high half
    write(addr + 1, data & 0x00FF);  // Write low half
  }

  uint16_t readShort(uint16_t addr) {
    uint16_t data = 0x0000;

    data |= (read(addr) << 8);
    data |= read(addr + 1);

    return data;
  }

  void readExternal(uint16_t addr, uint8_t size, uint8_t *buffer)
  {
    i2c::start();
    i2c::addr(EEPROM_ADDR | 1);
    i2c::write((uint8_t)(addr >> 8));
    i2c::write((uint8_t)(addr & 0xFF));
    i2c::start();

    for (uint8_t i = 0; i < size; i++) {
      bool ack = (i == size - 1) ? NACK : ACK;

      buffer[i] = i2c::read(ack);
    }

    i2c::stop();
  }
}