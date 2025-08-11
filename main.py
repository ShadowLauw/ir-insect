from camera import CameraController
from gui import GUI
from img_processor import ImageProcessor


def main():
    camera = CameraController()
    img_processor = ImageProcessor()
    app = GUI(camera, img_processor)
    app.run()


if __name__ == "__main__":
    main()
