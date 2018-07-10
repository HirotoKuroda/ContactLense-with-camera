import cv2 as cv


class Src:
    def __init__(self, img):
        # 通常
        self.img = img

        self.copy = self.img.copy()
        self.result = self.img.copy()

        self.h = self.img.shape[0]
        self.w = self.img.shape[1]

    def set_eye(self, ly, lx, ry, rx, ll, rl):
        self.left = Eye(ly, lx, ll)
        self.right = Eye(ry, rx, rl)

    def set_skin(self, color):
        self.skin = color


class Eye:
    def __init__(self, y, x, length):
        self.x = x
        self.y = y
        self.length = int(length * 2.4)

    def set_bright(self, bright):
        self.bright = bright


# ================================================================
class Contact:
    def __init__(self, img):
        self.img = cv.cvtColor(img, cv.COLOR_BGRA2GRAY)

    def resize(self, ll, rl):
        self.left = Size(cv.resize(self.img, (ll, ll)))
        self.right = Size(cv.resize(self.img, (rl, rl)))


class Size:
    def __init__(self, img):
        self.img = img
        self.length = img.shape[0]


# ================================================================
class Mask:
    # <value> - マスクの二値化された値(1 or 0)
    def __init__(self, value, h, w):
        self.value = value
        self.h, self.w = h, w
