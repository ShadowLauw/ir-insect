import datetime
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from picamera2.outputs import FileOutput


class CameraController:
    def __init__(self):
        self.picam2 = Picamera2()
        self.is_recording = False
        self.picam2.configure(
            self.picam2.create_preview_configuration(
                main={"format": "RGB888", "size": (640, 480)}
            )
        )
        self.picam2.start()

    def get_frame(self):
        frame = self.picam2.capture_array()
        return frame

    def take_picture(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.picam2.switch_mode_and_capture_file("still", f"image_{timestamp}.jpg")

    def toggle_recording(self):
        if self.is_recording:
            self.picam2.stop_recording()
            self.is_recording = False
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"video_{timestamp}.avi"
            self.picam2.start_recording(MJPEGEncoder(), FileOutput(filename))
            self.is_recording = True

        return self.is_recording
