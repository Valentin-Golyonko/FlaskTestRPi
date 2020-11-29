from time import sleep

from gpiozero import ToneBuzzer
from gpiozero.tones import Tone

tone_buzzer = ToneBuzzer(27)

for _ in range(2):
    tone_buzzer.play(Tone("C4"))
    sleep(0.15)
    tone_buzzer.play(Tone("G4"))
    sleep(0.15)
    tone_buzzer.play(Tone("F4"))
    sleep(0.15)

    tone_buzzer.stop()
    sleep(1)
