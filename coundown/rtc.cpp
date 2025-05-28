#include <stdint.h>
#include "rtc.h"
#include "base.h"
#include "display.h"

namespace rtc
{
  void setup()
  {
    RTC_WRITE(REG_CONTROL_1, 0x58);
    RTC_WRITE(REG_CONTROL_1, 0x80);
    RTC_WRITE(REG_CONTROL_2, 0x00);
    RTC_WRITE(REG_CONTROL_3, 0x00);
  }

  void setAlarm(uint8_t hourBCD, uint8_t minuteBCD)
  {
    RTC_WRITE(REG_CONTROL_1, 0b10000010);
    RTC_WRITE(0x0B, hourBCD);        
    RTC_WRITE(0x0A, minuteBCD);        
  }

  void setTimer(uint8_t source, uint8_t period)
  {
    RTC_WRITE(REG_CONTROL_2, (1 << RTC_CTAIE));
    RTC_WRITE(REG_TMR_A_FREQ_CTRL, source);
    RTC_WRITE(REG_TMR_A_REG, period);              
    RTC_WRITE(REG_TMR_CLKOUT_CTRL, 0b00111010);
  }

  void setTime(DateTime time, uint8_t weekday, uint8_t minutes, uint8_t seconds)
  {
    RTC_WRITE(REG_YEARS,      DecToBCD(time.year));
    RTC_WRITE(REG_MONTHS,     DecToBCD(time.month));
    RTC_WRITE(REG_WEEKDAYS,   DecToBCD(weekday));
    RTC_WRITE(REG_DAYS,       DecToBCD(time.day));
    RTC_WRITE(REG_HOURS,      DecToBCD(time.hour));
    RTC_WRITE(REG_MINUTES,    DecToBCD(minutes));
    RTC_WRITE(REG_OS_SECONDS, DecToBCD(seconds));
  }

  DateTime getTime() 
  {
    i2c::start();
    i2c::addr(RTC_ADDR);
    i2c::write(REG_HOURS);
    i2c::stop();

    DateTime dateTime = DateTime();

    i2c::start();
    i2c::addr(RTC_ADDR | 1);
    dateTime.hour =   BCDToDec(i2c::read(ACK));
    dateTime.day =    BCDToDec(i2c::read(ACK));
    i2c::read(ACK); // Skip weekdays
    dateTime.month =  BCDToDec(i2c::read(ACK));
    dateTime.year =   BCDToDec(i2c::read(NACK));

    return dateTime;
  }

  uint8_t getMinutes() 
  {
    i2c::start();
    i2c::addr(RTC_ADDR);
    i2c::write(REG_MINUTES);
    i2c::stop();

    i2c::start();
    i2c::addr(RTC_ADDR | 1);
    return BCDToDec(i2c::read(NACK));
  }

  void debugTime()
  {
    display::setEnabled(true);
    display::clear(1);
    display::selectPort(1);
    display::push(getTime().hour * 100 + getMinutes());
  }
}