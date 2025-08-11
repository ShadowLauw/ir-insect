from camera import CameraController
from gui import GUI


def main():
    camera = CameraController()
    app = GUI(camera)
    app.run()


if __name__ == "__main__":
    main()
