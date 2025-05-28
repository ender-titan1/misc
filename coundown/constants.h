#ifndef CONSTANTS
  #define CONSTANTS

#define SEG_A 0b00100000
#define SEG_B 0b01000000
#define SEG_C 0b00000100
#define SEG_D 0b00001000
#define SEG_E 0b00010000
#define SEG_F 0b00000001
#define SEG_G 0b00000010

#define RCLK 4
#define SRCLK 7
#define SER 14
#define SEL_A 16
#define SEL_B 15
#define OE 9

const char DIGITS[] = {
  0b11111111 & ~(SEG_G),
  SEG_B | SEG_C,
  SEG_A | SEG_B | SEG_G | SEG_E | SEG_D,
  SEG_A | SEG_B | SEG_C | SEG_G | SEG_D,
  SEG_F | SEG_B | SEG_G | SEG_C,
  SEG_A | SEG_F | SEG_G | SEG_C | SEG_D,
  0b11111111 & ~(SEG_B),
  SEG_A | SEG_B | SEG_C,
  0b11111111,
  0b11111111 & ~(SEG_E),
  0b00000000,
};

#endif