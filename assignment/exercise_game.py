"""
Response time - single-threaded
"""

from machine import Pin
import time
import random
import json

import network
import urequests
import binascii
import asyncio


# WiFi credentials
ssid = "jake (2)"
passw = ""
DNS = "8.8.8.8"
# setting number of flashes to 10
N: int = 10
sample_ms = 10.0
on_ms = 500
# database url
data_url = "https://mini-2024-d8147-default-rtdb.firebaseio.com/"

# WiFi connection function
async def connect_wifi():
    print(f"Connecting to WiFi {ssid}")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, passw)
    
    while not sta_if.isconnected():
        print(f"Still trying to connect to {ssid}")
        await asyncio.sleep_ms(1000)

    print(f"Connected to {ssid}")
    print(f"Setting DNS {DNS}")
    cfg = list(sta_if.ifconfig())
    cfg[-1] = DNS
    sta_if.ifconfig(cfg)

def upload_data(data: dict) -> None:
    urequests.post(data_url + ".json", json=data)



def random_time_interval(tmin: float, tmax: float) -> float:
    """return a random time interval between max and min"""
    return random.uniform(tmin, tmax)


def blinker(N: int, led: Pin) -> None:
    # %% let user know game started / is over

    for _ in range(N):
        led.high()
        time.sleep(0.1)
        led.low()
        time.sleep(0.1)


def write_json(json_filename: str, data: dict) -> None:
    """Writes data to a JSON file.

    Parameters
    ----------

    json_filename: str
        The name of the file to write to. This will overwrite any existing file.

    data: dict
        Dictionary data to write to the file.
    """

    with open(json_filename, "w") as f:
        json.dump(data, f)


def scorer(t: list[int | None]) -> None:
    # %% collate results
    misses = t.count(None)
    print(f"You missed the light {misses} / {len(t)} times")

    t_good = [x for x in t if x is not None]

    if t_good:
        min_time = min(t_good)
        max_time = max(t_good)
        avg_time = sum(t_good) / len(t_good)

        print(f"Min response time: {min_time} ms")
        print(f"Max response time: {max_time} ms")
        print(f"Avg response time: {avg_time:.2f} ms")
    else:
        print("No valid responses, all were missed.")
        min_time = max_time = avg_time = None

    print(t_good)


    # add key, value to this dict to store the minimum, maximum, average response time
    # and score (non-misses / total flashes) i.e. the score a floating point number
    # is in range [0..1]
    data = {
        "min": min_time,
        "max": max_time,
        "avg": avg_time,
    }

    # %% make dynamic filename and write JSON

    now: tuple[int] = time.localtime()

    now_str = "-".join(map(str, now[:3])) + "T" + "_".join(map(str, now[3:6]))
    filename = f"score-{now_str}.json"

    print("write", filename)

    write_json(filename, data)

    upload_data(data)


if __name__ == "__main__":
    # using "if __name__" allows us to reuse functions in other script files

    asyncio.run(connect_wifi())

    print(f"Starting game")

    led = Pin("LED", Pin.OUT)
    button = Pin(12, Pin.IN, Pin.PULL_UP)

    t: list[int | None] = []

    blinker(3, led)

    for i in range(N):
        time.sleep(random_time_interval(0.5, 5.0))

        led.high()

        tic = time.ticks_ms()
        t0 = None
        while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
            if button.value() == 0:
                t0 = time.ticks_diff(time.ticks_ms(), tic)
                led.low()
                break
        t.append(t0)

        led.low()

    blinker(5, led)

    scorer(t)
