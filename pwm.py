import RPi.GPIO as GPIO


class PWMController:
    """
    Controls a PWM output on a specified GPIO pin

    Supports manual or auto mode, with configurable frequency and duty cycle.
    Can start/stop PWM and update frequency or duty dynamically.
    """
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
        """Initialize PWM controller with pin, frequency, duty, and min/max ranges"""
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
        """Start or stop PWM output"""
        if self.enabled:
            self.pwm.stop()
            self.enabled = False
        else:
            self.pwm.start(self.duty)
            self.enabled = True

    def toggle_mode(self):
        """Switch PWM mode between 'auto' and 'manual'"""
        self.mode = "manual" if self.mode == "auto" else "auto"

    def update_freq(self, freq):
        """Update PWM frequency"""
        self.freq = round(float(freq))
        self.pwm.ChangeFrequency(self.freq)

    def update_duty(self, duty):
        """Update PWM duty cycle"""
        self.duty = round(float(duty))
        self.pwm.ChangeDutyCycle(self.duty)

    def stop(self):
        """Stop PWM and clean up GPIO (must be called on exit)"""
        self.pwm.stop()
        GPIO.cleanup()
