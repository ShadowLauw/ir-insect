import cv2


class ImageProcessor:
    def __init__(self, blur_ksize=3, equalize=True, palette=None):
        self.blur_ksize = blur_ksize
        self.equalize = equalize
        self.palette = palette

    def set_palette(self, palette):
        self.palette = palette

    def process(self, frame):
        if frame.dtype != "uint8":
            frame = frame.astype("uint8")
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        if self.equalize:
            gray = cv2.equalizeHist(gray)
        gray = cv2.GaussianBlur(gray, (self.blur_ksize, self.blur_ksize), 0)
        output = cv2.resize(gray, (640, 480), interpolation=cv2.INTER_LANCZOS4)

        if self.palette is not None:
            output = cv2.applyColorMap(output, self.palette)

        return output
