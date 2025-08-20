import cv2


class ImageProcessor:
    def __init__(self, blur_ksize=3, equalize=True, palette=None):
        self.blur_ksize = blur_ksize
        self.equalize = equalize
        self.palette = palette

    def set_palette(self, palette):
        self.palette = palette

    def process(self, frame):
        output = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_LANCZOS4)
        if self.palette is not None:
            output = cv2.cvtColor(output, cv2.COLOR_RGB2GRAY)
            if self.equalize:
                output = cv2.equalizeHist(output)
            output = cv2.GaussianBlur(output, (self.blur_ksize, self.blur_ksize), 0)

            if self.palette != "Grayscale":
                output = cv2.applyColorMap(output, self.palette)

        return output
