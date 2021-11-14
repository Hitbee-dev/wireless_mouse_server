import glob
import cv2
import natsort
def mosaic(src, ratio=0.1):
    small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
    return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

image_dirs = glob.glob("./data/*.png")
image_dirs = natsort.natsorted(image_dirs)
for i, dir in enumerate(image_dirs):
    gray_img = cv2.imread(dir, 0)
    w, h = gray_img.shape
    resize = 500
    rx, ry = (w // 2 - resize // 2, h // 2 - resize // 2)
    rect_img = gray_img[rx:rx+resize, ry:ry+resize].copy()
    mosaic_img = mosaic(rect_img, 0.05)
    norm_lv = 255//15
    norm_img = mosaic_img // norm_lv * norm_lv
    print(norm_img.shape)
    cv2.imwrite(f"./mosaic_data/{i}_img.png", norm_img)
