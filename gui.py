from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from camera import CameraController
from img_processor import ImageProcessor
from pwm import PWMController
from utils.colors import PALETTES


class GUI:
    def __init__(
        self,
        camera: CameraController,
        img_processor: ImageProcessor,
        pwm_controller: PWMController,
    ):
        self.root = Tk()
        self.root.title("IR Insect Detector")
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.root.bind("<Key>", self.key_handler)

        self.img_label = Label(self.mainframe)
        self.img_label.grid(row=0, column=0)

        self.camera = camera
        self.img_processor = img_processor
        self.pwm_controller = pwm_controller

        self.palette, self.palette_name = PALETTES[0]

        self.setup_settings_panel()

    def setup_settings_panel(self):
        self.settings_frame = ttk.Frame(self.mainframe)
        self.settings_frame.grid(row=0, column=1, sticky=(N, S), padx=10)

        self.setup_palette_selector()
        self.setup_action_buttons()
        self.setup_pwm_controls()

    def setup_palette_selector(self):
        ttk.Label(self.settings_frame, text="🎨 Select palette").pack(pady=5)
        palette_names = [name for _, name in PALETTES]
        self.palette_combo = ttk.Combobox(
            self.settings_frame, values=palette_names, state="readonly"
        )
        self.palette_combo.set(self.palette_name)  # default value
        self.palette_combo.pack(pady=5)
        self.palette_combo.bind("<<ComboboxSelected>>", self.on_palette_selected)

    def on_palette_selected(self, event):
        index = self.palette_combo.current()
        self.palette, self.palette_name = PALETTES[index]
        self.img_processor.set_palette(self.palette)
        self.update_image()

    def setup_action_buttons(self):
        ttk.Button(
            self.settings_frame, text="📸 Picture (P)", command=self.camera.take_picture
        ).pack(pady=5)
        self.record_button = ttk.Button(
            self.settings_frame, text="🎥 Record (R)", command=self.toggle_recording
        )
        self.record_button.pack(pady=5)

    def toggle_recording(self):
        started = self.camera.toggle_recording()
        if started:
            self.record_button["text"] = "🛑 Stop Recording (R)"
        else:
            self.record_button["text"] = "🎥 Record (R)"

    def key_handler(self, event: Event):
        key = event.char.lower()
        match key:
            case "r":
                self.toggle_recording()
            case "p":
                self.camera.take_picture()

    def setup_pwm_controls(self):
        self.pwm_label = ttk.Label(self.settings_frame, text="PWM : Inactive (GPIO 18)")
        self.pwm_label.pack(pady=5)
        ttk.Button(
            self.settings_frame, text="Toggle PWM", command=self.toggle_pwm
        ).pack(pady=5)

        # PWM Mode button
        self.pwm_auto_var = BooleanVar(value=self.pwm_controller.mode == "auto")
        ttk.Checkbutton(
            self.settings_frame,
            text="PWM Auto mode",
            command=self.toggle_pwm_mode,
            variable=self.pwm_auto_var,
        ).pack(pady=5)

        # Frequency
        ttk.Label(self.settings_frame, text="Frequency (Hz)").pack(pady=5)
        self.pwm_freq_scale = ttk.Scale(
            self.settings_frame,
            from_=self.pwm_controller.freq_min,
            to=self.pwm_controller.freq_max,
            orient=HORIZONTAL,
            command=self.on_pwm_freq_change,
        )
        self.pwm_freq_scale.set(self.pwm_controller.base_freq)
        self.pwm_freq_scale.state(["disabled"])
        self.pwm_freq_scale.pack(pady=5)

        # Duty cycle
        ttk.Label(self.settings_frame, text="Duty Cycle (%)").pack(pady=5)
        self.pwm_duty_scale = ttk.Scale(
            self.settings_frame,
            from_=self.pwm_controller.duty_min,
            to=self.pwm_controller.duty_max,
            orient=HORIZONTAL,
            command=self.on_pwm_duty_change,
        )
        self.pwm_duty_scale.set(self.pwm_controller.base_duty)
        self.pwm_duty_scale.state(["disabled"])
        self.pwm_duty_scale.pack(pady=5)

    def toggle_pwm(self):
        self.pwm_controller.toggle()
        self.update_pwm_text()

    def update_pwm_text(self):
        if self.pwm_controller.enabled:
            self.pwm_label["text"] = (
                f"PWM : {self.pwm_controller.freq} Hz {self.pwm_controller.duty} %"
            )
        else:
            self.pwm_label["text"] = f"PWM : Inactive (GPIO {self.pwm_controller.pin})"

    def toggle_pwm_mode(self):
        self.pwm_controller.toggle_mode()
        is_auto = self.pwm_auto_var.get()

        if is_auto:
            self.pwm_duty_scale.set(self.pwm_controller.base_duty)
            self.pwm_freq_scale.set(self.pwm_controller.base_freq)

        for widget in (self.pwm_freq_scale, self.pwm_duty_scale):
            widget.state(["disabled"] if is_auto else ["!disabled"])

    def on_pwm_freq_change(self, value):
        self.pwm_controller.update_freq(value)
        self.update_pwm_text()

    def on_pwm_duty_change(self, value):
        self.pwm_controller.update_duty(value)
        self.update_pwm_text()

    def update_image(self):
        frame = self.camera.get_frame()
        frame = self.img_processor.process(frame)
        im_pil = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=im_pil)
        self.img_label.imgtk = imgtk
        self.img_label["image"] = imgtk

        self.root.after(100, self.update_image)

    def close(self):
        self.pwm_controller.stop()
        self.camera.stop()
        self.root.destroy()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.update_image()
        self.root.mainloop()
