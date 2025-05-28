#include <Arduino.h>
#include <avr/interrupt.h>
#include <avr/sleep.h>
#include "ssd1306.h"

#include "base.h"
#include "constants.h"
#include "display.h"
#include "rtc.h"
#include "interface.h"

#define DEBOUNCE_MILLIS 75

volatile uint16_t countdown = 0;
volatile bool shouldHandleInput = false;
volatile bool shouldHandleSleep = false;
volatile bool update = false;
volatile bool disabled = false;
volatile uint8_t inputCode = 0;
unsigned long inputMillis = 0;
bool debouncing = false;

void setSleepAlarm()
{
  rtc::setAlarm(rtc::DecToBCD(23), rtc::DecToBCD(0)); 
}

void initMCU() 
{
  pinMode(SEL_A, OUTPUT);
  pinMode(SEL_B, OUTPUT);
  pinMode(SER, OUTPUT);
  pinMode(SRCLK, OUTPUT);
  pinMode(RCLK, OUTPUT);
  pinMode(OE, OUTPUT);

  display::setEnabled(true);
  display::clearAll();
  display::selectPort(1);

  // 100 kHz I2C mode
  TWBR = 0x48;
  TWSR &= ~((1 << TWPS0 | 1 << TWPS1));

  //eeprom::writeShort(0x00, 935);

  rtc::setup();
  setSleepAlarm();
  rtc::setTimer(TMR_SRC_MINUTES, 60);

  i2c::start();
  i2c::addr(0x70);
  i2c::write(0b00001111);
  i2c::stop();
}

void initInterrupts()
{
  pinMode(2, INPUT); // Use pin 2 for INT0
  pinMode(3, INPUT); // Use pin 3 for INT1

  EIMSK |= (1 << INT0) | (1 << INT1); // Enable INT0 & INT1 interrupt
  EICRA = 0b00001000; // INT0 triggered on low signal, INT1 triggered on falling edge

  sei(); // Enable global interrupts
}

void handleSleep()
{
  if (disabled) 
  {
    display::setEnabled(true);
    setSleepAlarm();
    update = true;
    disabled = false;
  }
  else 
  {
    display::clearAll();
    display::setEnabled(false);
    rtc::setAlarm(rtc::DecToBCD(6), rtc::DecToBCD(1));
    interface::clear();
    disabled = true;
  }

  cli();
  eeprom::write(0x04, disabled);
  sei();
}

uint8_t getExtenderInput()
{
  // Get get status byte from extender
  i2c::start();
  i2c::addr(0x70 | 1);
  uint8_t byte = i2c::read(NACK);
  i2c::stop();

  return(~byte & 0x0F); // The inverted lower nybble of this byte identifes which buttons are being pressed (as the button inputs are active LOW)
}

void handleInput()
{
  inputMillis = millis();
  debouncing = true;
  shouldHandleInput = false;
}

void handleDebounce()
{
  if (millis() - inputMillis > DEBOUNCE_MILLIS * 4)
  {
    debouncing = false;
  }

  if (millis() - inputMillis > DEBOUNCE_MILLIS) return;

  uint8_t code = getExtenderInput();

  if (code != inputCode) return;

  interface::handleInput(code);
  debouncing = false;
}

int main() 
{
  initMCU();

  countdown = eeprom::readShort(0x00);
  disabled = eeprom::read(0x04);
  update = true;

  initInterrupts();

  interface::setup();
  interface::topLevelMenu();

  //DateTime time;
  //time.day = 29;
  //time.month = 4;
  //time.year = 25;
  //time.hour = 20;
  //rtc::setTime(time, 2, 23, 0);

  while (true) 
  {
    if (shouldHandleInput) 
    {
      handleInput();
    }

    if (debouncing)
    {
      handleDebounce();
    }

    if (shouldHandleSleep)
    {
      handleSleep();
      shouldHandleSleep = false;
      continue;
    }

    if (disabled) continue;
    if (!update) continue;

    cli();
    eeprom::writeShort(0x00, countdown);
    sei();

    display::selectPort(1);
    display::push(countdown);
    display::selectPort(2);
    display::push(countdown / 24);

    update = false;
  }


  return 0;
}

// RTC Interrupt
ISR(INT0_vect) 
{
  // Get the RTC's control_2 register to check flags
  i2c::start();
  i2c::addr(RTC_ADDR);
  i2c::write(REG_CONTROL_2);
  i2c::stop();

  i2c::start();
  i2c::addr(RTC_ADDR | 1);
  uint8_t control_2 = i2c::read(NACK);
  i2c::stop();

  RTC_WRITE(REG_CONTROL_2, (1 << RTC_CTAIE)); // Clear flags

  if ((control_2 & (1 << RTC_CTAF)) != 0) {
    countdown--;
    update = true;
    return;
  }

  if ((control_2 & (1 << RTC_AF)) != 0) {
    shouldHandleSleep = true;
  }
}

// Extender Interrupt
ISR(INT1_vect)
{
  uint8_t code = getExtenderInput();

  inputCode = code;
  shouldHandleInput = true;  
}
