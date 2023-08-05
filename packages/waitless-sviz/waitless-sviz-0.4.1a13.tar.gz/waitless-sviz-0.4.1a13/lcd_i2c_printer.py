import machine
import utime as time

from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd


I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

SDA = machine.Pin(8)
SCL = machine.Pin(9)

i2c = I2C(0, sda=machine.Pin(8), scl=machine.Pin(9), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)


def loop(list): # Iter lists in eternal way
    while True:
        for item in list:
            yield item


def print_on_lcd_dumb(text): # Simplier write on LCD
    reset_waiting()
    lcd.clear()
    lcd.putstr(text)


def print_on_lcd(text1, text2 = '', centered = True): # Write by lines
    spaces_to_center = I2C_NUM_COLS
    if centered == False:
        spaces_to_center = 0

    reset_waiting()
    lcd.clear()
    lcd.move_to(0,0) 
    lcd.putstr(text1.center(spaces_to_center))
    lcd.move_to(0,1)
    lcd.putstr(text2.center(spaces_to_center))


def waiting_message(message): #Print on LCD and cursor bliking and the end
    reset_waiting()
    lcd.clear()
    lcd.putstr(message)
    lcd.blink_cursor_on()


def reset_waiting():  #Erase cursor when is blinking 
    lcd.hide_cursor()
    time.sleep(0.1)
    lcd.clear()
    

def moving_message(message1, line = 1, refresh = 0.4, message2 = '', t_expire=60):
    reset_waiting()
    lcd.clear()
    if line != 0 and line !=1 :
        raise ValueError('Only 0 or 1 are allowed for line argument')
    lcd.clear()
    spaces = I2C_NUM_COLS - len(message1)
    chain_text = list(message1 + ' ' * (I2C_NUM_COLS + 1))[::-1]
    
    if line == 0:
        line2 = 1
    else:
        line2 = 0
        
    lcd.move_to(0,line2)    
    lcd.putstr(message2)
    while t_expire > 0: ### Ojo usar asíncrono o poner tope
        chtr = loop(chain_text)
        for i in range(I2C_NUM_COLS + 1):
            lcd.move_to(I2C_NUM_COLS -i,line)
            lcd.putchar(next(chtr))
            
        last = chain_text.pop()
        chain_text.insert(0, last)
        time.sleep(refresh)
        t_expire -= refresh


def insert_message(message, col, line): #Insert part movil on a string improve
    lcd.move_to(col,line)               # quality of visibility
       
    for letter in message:
        lcd.putchar(letter)
        col += 1
        lcd.move_to(col,line)       
    

def show_wait_time(arrivals, delay=60): # Optimized to show arrivals data
    matrix_lcd = []
    
    for arrival in arrivals:
        disp_spaces = I2C_NUM_COLS - (len(arrival[0]) +
                                      len(arrival[1])
                                     )
           
        matrix_lcd.append("{0}{2}{1}".format(arrival[0],
                                             arrival[1],
                                             ' ' * disp_spaces
                                             )
                          )
       
        step = loop(matrix_lcd)
        ant  = next(step)
  
    if len(matrix_lcd) > 2:
        while delay > 0:
             post = next(step)
             print_on_lcd_dumb(ant + post)
             ant = post
             time.sleep(2)
             delay -= 2
             
    elif len(matrix_lcd) == 2:
        post = next(step)
        print_on_lcd_dumb(ant + post)
        
    elif len(matrix_lcd) == 1:
        print_on_lcd_dumb(ant)
        
    else: 
        waiting_message('Configure otra  parada. Reinicie')
        
    return delay


async def info_during_setup(lines):   #Asynchronous message carrousel 
    import uasyncio as asyncio
    global finish_countdown
    from configure import finish_countdown
        
    
    def optimize(text):
        text = text + ((I2C_NUM_COLS - len(text)) * ' ')
        return text
    
    if len(lines) % 2 == 1:           #Return None    
        lines.append('')
        
    step = loop(lines)
    
    while finish_countdown == False:
        ant = next(step)               
        post = next(step)
        print_on_lcd_dumb(optimize(ant) + optimize(post))
        await asyncio.sleep(2)
        from configure import finish_countdown

        