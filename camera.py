from datetime import datetime
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput


class CameraController:
    def __init__(self):
        self.picam2 = Picamera2()
        self.is_recording = False

        self.preview_config = self.picam2.create_preview_configuration(
            main={"format": "RGB888", "size": (640, 480)}
        )
        self.record_config = self.picam2.create_video_configuration(
            main={"size": (1920, 1080)}, encode="main"
        )

        self.set_mode_preview()

    def set_mode_preview(self):
        self.picam2.stop()
        self.picam2.configure(self.preview_config)
        self.picam2.start()

    def set_mode_record(self):
        self.picam2.stop()
        self.picam2.configure(self.record_config)

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
            self.set_mode_preview()
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.filename = f"video_{timestamp}.h264"
            self.set_mode_record()
            self.picam2.start_recording(
                H264Encoder(bitrate=10000000), FileOutput(self.filename)
            )
            self.is_recording = True

        return self.is_recording

    def stop(self):
        self.picam2.close()
