import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP  
import math
import time
from adafruit_mcp3xxx.analog_in import AnalogIn

#create the spi bus
spi = busio.SPI(clock = board.SCK, MISO = board.MISO, MOSI = board.MOSI)

#create the css (chip select)
cs = digitalio.DigitalInOut(board.D5)

#create the mcp object 
mcp = MCP.MCP3008(spi, cs)

#create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P0)

def mittaus():
    for i in range(1):
        thermistor = AnalogIn(mcp, MCP.P0)

        thermistor.value

        # Palauttaa nollan jos ei arvoa.
        if thermistor.value == 0.0:
            return(0.0)
        
        else:
            R = 10000 / (65535/thermistor.value - 1)

            def steinhart_temperature_C(r, Ro = 10000, To = 0.5, beta = 3860.0):
                steinhart = math.log(r / Ro) / beta
                steinhart += 1.0 / (To + 273.15)
                steinhart = (1.0 / steinhart) - 273.15
                return steinhart
        R = 10000 / (65535/thermistor.value -1)
        p = steinhart_temperature_C(R)
        return(p)

def main():
    mittaus()

main()