import time


def progress_bar(draw, x, y, width, height, progress, color) -> None:
    draw.rectangle((x, y, x + width, y + height), outline=0, fill=(0, 0, 0))
    draw.rectangle((x, y, x + int(width * progress), y + height), outline=0, fill=color)


def draw_menu(draw, temp_c, humidity_p, dew_point_c, last_successful_read_time, fonts, activation_c_over_dew,
              temp_activation_c_over_dew) -> bool:
    now = time.time()
    if now - last_successful_read_time > 10:
        draw.text((5, 5), "Error reading data", font=fonts.get_font(), fill=(255, 255, 255))
        return False

    activation_temp = dew_point_c + activation_c_over_dew
    draw.text((5, 5), "Temperatur: {:.1f} C".format(temp_c), font=fonts.get_font(), fill=(255, 255, 255))
    draw.text((5, 20), "Luftfeuchtigkeit: {}%".format(humidity_p), font=fonts.get_font(), fill=(255, 255, 255))
    draw.text((5, 35), "Taupunkt: {:.1f} C".format(dew_point_c), font=fonts.get_font(), fill=(255, 255, 255))
    draw.text((5, 50), "Messung vor {:.1f} Sekunden".format(now - last_successful_read_time), font=fonts.get_font(),
              fill=(255, 255, 255))
    draw.text((5, 65), "Aktivierung bei {:.1f} C".format(activation_temp), font=fonts.get_font(), fill=(255, 255, 255))

    # Calculate the color
    # Full green = > 10°C over dew point
    # Full red = < 0°C over dew point
    temperature_over_activation = temp_c - activation_temp
    R = 0
    G = 0
    B = 0
    # Calculate gradient
    if temperature_over_activation > 10:
        R = 255
    elif temperature_over_activation < 0:
        G = 255
    else:
        G = 255 - R
        R = int(255 * (temperature_over_activation / 10))

    draw.text((5, 80), "Konfigurations Delta: {:.1f} C".format(activation_c_over_dew), font=fonts.get_font(),
              fill=(255, 255, 255))
    progress_bar(draw, 5, 95, 128, 5, temp_activation_c_over_dew / 10, (0, 255, 255))

    # Draw a big ACTIVE or INACTIVE text (depending on the temperature)
    if temp_c <= activation_temp:
        draw.text((5, 100), "AKTIV", font=fonts.get_font_large(), fill=(0, 0, 255))
    else:
        draw.text((5, 100), "INAKTIV", font=fonts.get_font_large(), fill=(B, R, G))

    return True
