#ifndef RTC
  #define RTC

#include <stdint.h>
#include "base.h"

#define RTC_ADDR 0b11010000

#define REG_CONTROL_1         0x00
#define REG_CONTROL_2         0x01
#define REG_CONTROL_3         0x02
#define REG_OS_SECONDS        0x03
#define REG_MINUTES           0x04
#define REG_HOURS             0x05
#define REG_DAYS              0x06
#define REG_WEEKDAYS          0x07
#define REG_MONTHS            0x08
#define REG_YEARS             0x09

#define RTC_CTAIE             0x01
#define RTC_CTAF              0x06
#define RTC_AF                0x03

#define REG_TMR_CLKOUT_CTRL   0x0F
#define REG_TMR_A_FREQ_CTRL   0x10
#define REG_TMR_A_REG         0x11

#define TMR_SRC_MINUTES 0b00000011

#define RTC_WRITE(reg, data)  i2c::start(); \
                              i2c::addr(RTC_ADDR); \
                              i2c::write(reg); \
                              i2c::write(data); \
                              i2c::stop()


struct DateTime
{
  uint8_t hour;
  uint8_t day;
  uint8_t month;
  uint8_t year;
};

namespace rtc
{
  void setup();

  void setAlarm(uint8_t hourBCD, uint8_t minuteBCD);
  void setTimer(uint8_t source, uint8_t period);

  void setTime(DateTime time, uint8_t weekday, uint8_t minutes, uint8_t seconds);
  DateTime getTime();
  uint8_t getMinutes();

  void debugTime();

  inline uint8_t BCDToDec(uint8_t bcd) { return (bcd >> 4) * 10 + (bcd & 0x0F); }
  inline uint8_t DecToBCD(uint8_t decimal) { return ((decimal / 10) << 4) | (decimal % 10); }
}

#endif