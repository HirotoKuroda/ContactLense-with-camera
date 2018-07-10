import cv2 as cv

from classes import Mask, Src
from adjustment import adjustment
from detection import detection
from contact import contact


# ================================================================
def make_mask():
    mask_img = cv.imread('mask.jpg', -1)

    h, w = mask_img.shape[0], mask_img.shape[1]

    value = [[0 for i in range(w)] for j in range(h)]
    for y in range(h):
        for x in range(w):
            if mask_img[y, x] < 200:
                value[y][x] = 1
            else:
                value[y][x] = 0

    mask = Mask(value, h, w)

    return mask


# ================================================================
def camera(mask):
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FPS, 60)
    # cap.set(cv.CAP_PROP_FRAME_WIDTH, 1080 * 2)
    # cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1440 * 2)

    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

    ret, src = cap.read()
    imgX = src.copy()

    while 1:
        ret, img0 = cap.read()

        # WEBカメラ
        # img0 = img0[0:1440 * 2, 0:1080 * 2]
        # img2 = Image.fromarray(img0)
        # img3 = img2.rotate(90, expand=True)
        # imgX = np.asanyarray(img3)

        # 内蔵カメラ
        # トリミング(h:720, w:540)
        src = img0[int(img0.shape[0] / 2 - 360):int(img0.shape[0] / 2 + 360),
              int(img0.shape[1] / 2 - 270):int(img0.shape[1] / 2 + 270)]

        # WEBカメラ
        # src = cv.resize(imgX, (mask.w, mask.h))

        # マスクを被せた画像
        img = src.copy()
        for y in range(mask.h):
            for x in range(mask.w):
                if mask.value[y][x] == 1:
                    img[y, x] = [255, 255, 255]

        cv.imshow('TAKE: <SPACE-KEY>', cv.flip(img, 1))
        key = cv.waitKey(1)

        if key == ord(' '):
            break

    cv.destroyAllWindows()
    cap.release()

    cv.imshow('DECISION: <SPACE-KEY>', img)
    key = cv.waitKey(0)
    cv.destroyAllWindows()
    if key == ord(' '):
        # WEBカメラ
        # return imgX

        # 内蔵カメラ
        return src
    else:
        # 再帰
        return camera(mask)


# ================================================================
def main():
    mask = make_mask()

    src = Src(camera(mask))

    cv.imshow('-FACE-  continue-(Press eny key)', cv.resize(src.img, (540, 720)))
    cv.waitKey(0)
    cv.destroyAllWindows()

    # 中心判定
    detection(src)

    # 調節
    adjustment(src)

    print("left<y: {},  x: {}>,  right<y: {},  x: {}>".format(src.left.y, src.left.x, src.right.y, src.right.x))
    print("l_length: {},  r_length: {}".format(src.left.length, src.right.length))

    contact(src)

    # 拡大
    # img = cv.resize(src.result, (540, 720))
    # cv.imshow('-RESULT-  continue-(Press eny key)', img)

    # 通常
    cv.imshow('-RESULT-  continue-(Press eny key)', src.result)

    cv.waitKey(0)

    cv.imwrite("result.jpg", src.result)


# ================================================================

if __name__ == "__main__":
    main()
