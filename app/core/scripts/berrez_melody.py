from time import sleep

from gpiozero import TonalBuzzer
from gpiozero.tones import Tone


def alarm_buzzer_melody():
    tone_buzzer = TonalBuzzer(27)

    for _ in range(5):
        tone_buzzer.play(Tone("C4"))
        sleep(0.15)
        tone_buzzer.play(Tone("G4"))
        sleep(0.15)
        tone_buzzer.play(Tone("F4"))
        sleep(0.15)

        tone_buzzer.stop()
        sleep(2)
