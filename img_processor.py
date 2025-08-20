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

        gray = cv2.cvtColor(output, cv2.COLOR_RGB2GRAY)
        if self.equalize:
            gray = cv2.equalizeHist(gray)
        gray = cv2.GaussianBlur(gray, (self.blur_ksize, self.blur_ksize), 0)

        if self.palette is not None:
            if self.palette != "Grayscale":
                output_colormap = cv2.applyColorMap(gray, self.palette)
            else:
                output_colormap = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
        else:
            output_colormap = output.copy()

        # --- Highlight insects ---
        _, thresh = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            if cv2.contourArea(cnt) > 200:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(output_colormap, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return output_colormap