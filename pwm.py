import RPi.GPIO as GPIO


class PWMController:
    def __init__(
        self,
        pin=18,
        freq=1000,
        freq_min=500,
        freq_max=1500,
        duty=50,
        duty_min=0,
        duty_max=100,
    ):
        if freq_min > freq_max or freq > freq_max:
            raise ValueError("Invalid frequency parameters")
        self.pin = pin

        self.base_freq = freq
        self.freq_min = freq_min
        self.freq_max = freq_max

        self.base_duty = duty
        self.duty_min = duty_min
        self.duty_max = duty_max

        self.freq = freq
        self.duty = duty

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.freq)
        self.enabled = False
        self.mode = "auto"

    def toggle(self):
        if self.enabled:
            self.pwm.stop()
            self.enabled = False
        else:
            self.pwm.start(self.duty)
            self.enabled = True

    def toggle_mode(self):
        self.mode = "manual" if self.mode == "auto" else "auto"

    def update_freq(self, freq):
        self.freq = round(float(freq))
        self.pwm.ChangeFrequency(self.freq)

    def update_duty(self, duty):
        self.duty = round(float(duty))
        self.pwm.ChangeDutyCycle(self.duty)

    def stop(self):
        self.pwm.stop()
        GPIO.cleanup()
