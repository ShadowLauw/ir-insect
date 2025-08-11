from camera import CameraController
from gui import GUI
from img_processor import ImageProcessor
from pwm import PWMController


def main():
    camera = CameraController()
    img_processor = ImageProcessor()
    pwm_controller = PWMController()
    app = GUI(camera, img_processor, pwm_controller)
    app.run()


if __name__ == "__main__":
    main()
