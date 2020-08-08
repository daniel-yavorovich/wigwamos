import time
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class Screen:
    SCREEN_SHOW_TIMEOUT = 30
    I2C_ADDRESS = 0x3C

    # Raspberry Pi pin configuration:
    RST = None  # on the PiOLED this pin isnt used
    # Note the following are only used with SPI:
    DC = 23
    SPI_PORT = 0
    SPI_DEVICE = 0

    def __init__(self):
        self.display = Adafruit_SSD1306.SSD1306_128_64(rst=self.RST, i2c_address=self.I2C_ADDRESS)
        self.display.begin()
        self.display.clear()
        self.display.display()

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        self.width = self.display.width
        self.height = self.display.height
        self.image = Image.new('1', (self.width, self.height))

        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)

        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

        # Draw some shapes.
        # First define some constants to allow easy resizing of shapes.
        padding = -2
        self.top = padding
        self.bottom = self.height - padding
        # Move left to right keeping track of the current x position for drawing shapes.
        self.x = 0

        # Load default font.
        self.font = ImageFont.load_default()

    def display_show_multiline_text(self, lines):
        top = self.top
        top_step = 8

        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

        for line in lines:
            self.draw.text((self.x, top), line, font=self.font, fill=255)
            top += top_step

        # Display image.
        self.display.image(self.image)
        self.display.display()
        time.sleep(.1)

    def display_show_stats(self, alerts, day_count, progress_percentage, humidity, temperature, fan_speed_percent,
                           water_level):
        lines = []

        if not alerts:
            lines += ['All is fine', '']
        elif len(alerts) == 1:
            lines += [alerts[0], '']
        else:
            lines = alerts

        lines += [
            "{temperature}C   {humidity}%".format(temperature=temperature, humidity=humidity),
            "Fan speed: {}%".format(fan_speed_percent),
            "Water level: {}%".format(water_level),
            "Grow day: {day_count} ({progress_percentage}%)".format(day_count=day_count,
                                                                    progress_percentage=progress_percentage)
        ]

        self.display_show_multiline_text(lines)
