#include <Arduino.h>
#include "display.h"
#include "constants.h"

namespace display
{
  void selectPort(uint8_t port)
  {
    bool bitA = ((port - 1) & 0b00000001);
    bool bitB = ((port - 1) & 0b00000010);

    digitalWrite(SEL_A, bitA);
    digitalWrite(SEL_B, bitB);
  }

  void push(uint16_t block)
  {
    digitalWrite(RCLK, LOW);

    bool nonZero = false;
    for (int i = 3; i >= 0; i--) {
      uint16_t digit = ((uint16_t)(block / pow(10, i))) % 10;
  
      if (digit == 0) {
        if (!nonZero)
          digit = 10;
      }
      else {
        nonZero = true;
      }
  
      shiftOut(SER, SRCLK, MSBFIRST, DIGITS[digit]);
    }

    digitalWrite(RCLK, HIGH);
  }

  void pushArray(uint16_t *blocks, uint8_t size)
  {
    for (uint8_t i = 0; i < size; i++)
    {
      push(blocks[i]);
    }
  }


  void clear(uint8_t port)
  {
    selectPort(port);
    push(0);
    push(0);
    push(0);
    push(0);
  }

  void clearAll()
  {
    clear(1);
    clear(2);
    clear(3);
    clear(4);
  }

  void setEnabled(bool enabled)
  {
    digitalWrite(OE, !enabled);
  }
}