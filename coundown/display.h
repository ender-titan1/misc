#ifndef SEVENSEG
  #define SEVENSEG

#include <stdint.h>

namespace display
{
  void selectPort(uint8_t port);

  void push(uint16_t block);
  void pushArray(uint16_t *blocks, uint8_t size);

  void clear(uint8_t port);
  void clearAll();
  
  void setEnabled(bool enabled);
}

#endif