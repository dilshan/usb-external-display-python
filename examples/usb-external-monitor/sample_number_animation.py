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

START_DIGIT = 20
ANIMATION_DELAY = 0.1
DEVICE_PORT = '/dev/ttyACM0'


def animate_text(in_str, handle):
    direction = 1
    loop_count = 2
    left_pad, right_pad = 0, 10 - len(in_str)

    while loop_count > 0:
        out_str = (' ' * left_pad) + in_str + (' ' * right_pad)
        handle.show_message(out_str)

        if (left_pad == 0) and (loop_count == 1):
            break

        left_pad += direction
        right_pad += direction * -1
        time.sleep(ANIMATION_DELAY)

        if right_pad == 0:
            direction *= -1
            loop_count -= 1


start_digit = START_DIGIT
device_handle = counter_api.ExternalCounter(DEVICE_PORT)
while start_digit >= 0:
    animate_text(str(start_digit), device_handle)
    start_digit -= 1
