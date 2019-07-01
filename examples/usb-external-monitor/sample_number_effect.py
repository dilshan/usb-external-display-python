# *****************************************************************************
#  Copyright 2019 Dilshan R Jayakody. [jayakody2000lk@gmail.com]
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
# *****************************************************************************

import external_counter.external_counter as counter_api
import time

NUMBER_TO_DISPLAY = '1560'
FLY_SPEED = 0.03
DEVICE_PORT = '/dev/ttyACM0'


def move_char_to_pos(digit, pos, last_display_str, handle):
    current_pos = 9

    while current_pos >= pos:
        display_buffer = last_display_str[:current_pos]
        display_buffer += digit
        display_buffer += ' ' * (10 - current_pos)

        last_display_str = display_buffer[:10]
        handle.show_message(last_display_str)

        time.sleep(FLY_SPEED)
        current_pos -= 1

    return last_display_str


def show_number_fly_effect(in_str, handle):
    char_count_in_display = 0
    output_char_pos = 0
    last_display_str = ' ' * 10

    while output_char_pos < len(in_str):
        last_display_str = move_char_to_pos(in_str[output_char_pos], char_count_in_display, last_display_str, handle)
        output_char_pos += 1
        char_count_in_display += 1


device_handle = counter_api.ExternalCounter(DEVICE_PORT)
device_handle.clear_display()
show_number_fly_effect(NUMBER_TO_DISPLAY, device_handle)
