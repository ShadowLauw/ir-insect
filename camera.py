from picamera2 import Picamera2


class CameraController:
    def __init__(self):
        self.camera = Picamera2()
        self.picam2.configure(
            self.picam2.create_preview_configuration(
                main={"format": "RGB888", "size": (640, 480)}
            )
        )
        self.camera.start()

    def get_frame(self):
        frame = self.camera.capture_array()
        return frame
