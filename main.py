import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import st7735
from st7735 import ST7735

from dht22 import DHT
from ky040 import KY040
from menu import draw_menu


class Fonts:
    def __init__(self):
        self.font = ImageFont.load_default()
        self.font_large = ImageFont.load_default(16)

    def get_font(self):
        return self.font

    def get_font_large(self):
        return self.font_large


fonts = Fonts()


def init_display() -> (ImageDraw, Image, ST7735, int, int):
    display: ST7735 = st7735.ST7735(port=0, cs=0, dc=23, backlight=None, rst=24, width=128, height=160, rotation=90,
                                    invert=False,
                                    offset_top=0, offset_left=0)
    width: int = display.width
    height: int = display.height
    image: Image = Image.new('RGB', (width, height))
    image_draw: ImageDraw = ImageDraw.Draw(image)
    display.display(image)

    return image_draw, image, display, width, height


activation_c_over_dew = 2.0
temp_activation_c_over_dew = 2.0


def rotary_cb(rotation):
    global temp_activation_c_over_dew
    if rotation == KY040.CLOCKWISE:
        temp_activation_c_over_dew += 0.1
    else:
        temp_activation_c_over_dew -= 0.1
    print("New activation_c_over_dew: {:.1f}".format(temp_activation_c_over_dew))
    if temp_activation_c_over_dew < 0:
        temp_activation_c_over_dew = 0
    if temp_activation_c_over_dew > 10:
        temp_activation_c_over_dew = 10


def switch_cb():
    global activation_c_over_dew
    activation_c_over_dew = temp_activation_c_over_dew
    print("Activation_c_over_dew set to: {:.1f}".format(activation_c_over_dew))


# Main func
if __name__ == '__main__':
    dht = DHT()
    ky040 = KY040(5, 6, 13, rotaryCallback=rotary_cb, switchCallback=switch_cb)
    image_draw, image, display, width, height = init_display()

    # Selfcheck
    image_draw.text((0, 0), "Selfcheck in progress...", font=fonts.get_font(), fill="#FFFFFF")
    display.display(image)
    retry = 0
    while True:
        temp_c = dht.get_last_temperature_c()
        humidity_p = dht.get_last_humidity_p()
        dew_point_c = dht.get_last_dew_point_c()
        last_successful_read_time = dht.get_last_successful_read_time()
        if last_successful_read_time > 0:
            break
        image_draw.text((0, 0), "Selfcheck in progress...{}".format(retry), font=fonts.get_font(), fill="#FFFFFF")
        retry += 1
        if retry > 100:
            image_draw.text((0, 0), "Selfcheck failed", font=fonts.get_font(), fill="#FF0000")
            display.display(image)
            time.sleep(1)
            exit(1)
        time.sleep(1)

    while True:
        time.sleep(0.01)
        image_draw.rectangle((0, 0, width, height), outline=0, fill=0)

        temp_c = dht.get_last_temperature_c()
        humidity_p = dht.get_last_humidity_p()
        dew_point_c = dht.get_last_dew_point_c()
        last_successful_read_time = dht.get_last_successful_read_time()

        success = draw_menu(image_draw, temp_c, humidity_p, dew_point_c, last_successful_read_time, fonts,
                            activation_c_over_dew, temp_activation_c_over_dew)
        display.display(image)

        if not success:
            time.sleep(1)
            exit(1)
