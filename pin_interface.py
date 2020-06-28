from recorder import MIDIRecorder
import RPi.GPIO as GPIO
import os
import typer

app = typer.Typer()

input_pins = {
        'toggle_record': 7,
        'toggle_play': 11,
        'toggle_loop': 13,
        'increase_tempo': 15,
        'decrease_tempo': 19,
        'reset_tempo': 21,
        'shutdown': 24,
}
output_pins = {
        'led': 26
}

@app.command()
def start(bounce_time: int):
    # GPIO setup
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    for pin in input_pins.values():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    for pin in output_pins.values():
        GPIO.setup(pin, GPIO.OUT)

    print('loading')
    r = MIDIRecorder('/home/pi/test_midi_dir', 20, 20, 1, 0)
    GPIO.output(output_pins['led'], 1)

    GPIO.add_event_detect(input_pins['toggle_record'], GPIO.RISING, \
            callback=lambda: _r.toggle_record, bouncetime=bounce_time)
    GPIO.add_event_detect(input_pins['toggle_play'], GPIO.RISING, \
            callback=lambda: _r.toggle_play, bouncetime=bounce_time)
    GPIO.add_event_detect(input_pins['toggle_loop'], GPIO.RISING, \
            callback=lambda _ :r.toggle_loop, bouncetime=bounce_time)
    GPIO.add_event_detect(input_pins['increase_tempo'], GPIO.RISING, \
            callback=lambda _:r.change_speed(0.9), bouncetime=bounce_time)
    GPIO.add_event_detect(input_pins['decrease_tempo'], GPIO.RISING, \
            callback=lambda _:r.change_speed(1/0.9), bouncetime=bounce_time)
    GPIO.add_event_detect(input_pins['reset_tempo'], GPIO.RISING, \
            callback=lambda _:r.change_absolute_speed(1), bouncetime=bounce_time)
    GPIO.add_event_detect(input_pins['shutdown'], GPIO.RISING, \
            callback=lambda _:os.system('sudo shutdown -h now'), \
            bouncetime=bounce_time)
    print('loaded')

    while True:
        pass

if __name__ == '__main__':
    app()
