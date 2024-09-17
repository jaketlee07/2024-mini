#!/usr/bin/env python3
"""
PWM Tone Generator

based on https://www.coderdojotc.org/micropython/sound/04-play-scale/
"""

import machine
import utime

# GP16 is the speaker pin
SPEAKER_PIN = 16

# create a Pulse Width Modulation Object on this pin
speaker = machine.PWM(machine.Pin(SPEAKER_PIN))


def playtone(frequency: float, duration: float) -> None:
    speaker.duty_u16(1000)
    speaker.freq(frequency)
    utime.sleep(duration)


def quiet():
    speaker.duty_u16(0)


freq = [1319, 1175, 740, 831, 1109, 988, 587, 659, 988, 880, 554, 659, 880] # frequencies are obtained through sheet music
duration = [8, 8, 16, 16, 8, 8, 16, 16, 8, 8, 16, 16, 32]  # 8 represents a quarter note, 16 represents a half note and 32 is a whole note



print("Playing frequency (Hz):")

for i in range(13):
    print(freq[i])
    playtone(freq[i], ((duration[i]*4)/150)*0.9) # duration is adjusted for tempo
    quiet()
    

# Turn off the PWM
quiet()