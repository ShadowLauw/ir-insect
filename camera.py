from datetime import datetime
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput


class CameraController:
    """
    Simple wrapper around Picamera2 for preview, still capture, and video recording

    Features:
    - Live preview at low resolution
    - High-resolution video recording
    - Timestamped still images
    - Toggle recording on/off
    """
    def __init__(self):
        """Initialize CameraController with preview and recording configurations and start preview"""
        self.picam2 = Picamera2()
        self.is_recording = False

        # Configuration for live preview (low resolution, fast)
        self.preview_config = self.picam2.create_preview_configuration(
            main={"format": "RGB888", "size": (640, 480)}
        )
        # Configuration for video recording (higher resolution, encoded)
        self.record_config = self.picam2.create_video_configuration(
            main={"size": (1920, 1080)}, encode="main"
        )

        self.set_mode_preview()

    def set_mode_preview(self):
        """Switch camera to preview mode (used for live display)"""
        self.picam2.stop()
        self.picam2.configure(self.preview_config)
        self.picam2.start()

    def set_mode_record(self):
        """Prepare camera for recording (does not start recording yet)"""
        self.picam2.stop()
        self.picam2.configure(self.record_config)

    def get_frame(self):
        """Capture a single frame as a NumPy array"""
        frame = self.picam2.capture_array()
        return frame

    def take_picture(self):
        """Capture and save a still image with a timestamped filename"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.picam2.switch_mode_and_capture_file("still", f"image_{timestamp}.jpg")

    def toggle_recording(self):
        """
        Start or stop recording
        - If already recording: stop and return to preview mode
        - If not recording: start a new recording to a timestamped file
        """
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
        """Release camera resources (must be called on exit)"""
        self.picam2.close()
