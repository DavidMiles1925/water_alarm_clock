import RPi.GPIO as GPIO
import time

# GPIO to LCD mapping
LCD_RS = 7   # Pi pin 26
LCD_E  = 8   # Pi pin 24
LCD_D4 = 25  # Pi pin 22
LCD_D5 = 24  # Pi pin 18
LCD_D6 = 23  # Pi pin 16
LCD_D7 = 18  # Pi pin 12

# Device constants
LCD_CHR = True    # Character mode
LCD_CMD = False   # Command mode
LCD_CHARS = 16    # Characters per line (16 max)
LCD_LINE_1 = 0x80 # LCD memory location for 1st line
LCD_LINE_2 = 0xC0 # LCD memory location 2nd line

# Initialize and clear display
def lcd_init():
  lcd_write(0x33,LCD_CMD) # Initialize
  lcd_write(0x32,LCD_CMD) # Set to 4-bit mode
  lcd_write(0x06,LCD_CMD) # Cursor move direction
  lcd_write(0x0C,LCD_CMD) # Turn cursor off
  lcd_write(0x28,LCD_CMD) # 2 line display
  lcd_write(0x01,LCD_CMD) # Clear display
  time.sleep(0.0005)     # Delay to allow commands to process

def lcd_write(bits, mode):
# High bits
  GPIO.output(LCD_RS, mode) # RS

  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

# Toggle 'Enable' pin
  lcd_toggle_enable()

# Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

# Toggle 'Enable' pin
  lcd_toggle_enable()

def lcd_toggle_enable():
  time.sleep(0.0005)
  GPIO.output(LCD_E, True)
  time.sleep(0.0005)
  GPIO.output(LCD_E, False)
  time.sleep(0.0005)

def lcd_text(message,line):
  # Send text to display
  message = message.ljust(LCD_CHARS," ")

  lcd_write(line, LCD_CMD)

  for i in range(LCD_CHARS):
    lcd_write(ord(message[i]),LCD_CHR)