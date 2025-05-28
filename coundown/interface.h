#ifndef INTERFACE
  #define INTERFACE

#include <stdint.h>

#define OLED_ADDR 0b01111000
#define OLED_STOP_AUTOSCROLL 0x2E

namespace interface
{

  enum Menu : uint8_t
  {
    TOP_LEVEL = 0,
    SETTINGS = 1,
    ADJ_END = 2,
    ADJ_NEXT = 3,
    ALARM = 4,
    POWER_DOWN = 5
  };

  void setup();
  void handleInput(uint8_t code);
  uint8_t* loadImage(uint16_t addr);
  void topLevelMenu();
  void settingsMenu();
  void adjustmentMenu(Menu menu);
  void alarmMenu();
  void powerDownMenu();
  void clear();
  void updateCurrent();
}

#endif