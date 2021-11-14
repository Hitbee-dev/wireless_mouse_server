import glob
import natsort
from PIL import Image

ERROR = 5

img_dirs = glob.glob("./mosaic_data/*.png")
img_dirs = natsort.natsorted(img_dirs)

class LoopBreak(Exception):
    pass

for i, dir in enumerate(img_dirs):
    if i + 1 >= len(img_dirs):
        continue
    src = Image.open(img_dirs[i + 1])
    src_img = src.load()
    tgt = Image.open(dir)
    tgt_img = tgt.load()
    match = []
    moc_size = 20
    sw, sh = src.width // moc_size, src.height // moc_size
    tw, th = tgt.width // moc_size, tgt.height // moc_size
    tx, ty = -tw, -th
    
    for m in range(1, th * 2):
        ry = ty + m
        if ry < 0: ry = -ry
        else: ry = 0
        for n in range(1, tw * 2):
            rx = tx + n
            if rx < 0: rx = -rx
            else: rx = 0
            print(f"Image {i}")
            for sy in range(max(0, ty + m), min(sh, ty + m + th)):
                for sx in range(max(0, tx + n), min(sw, tx + n + tw)):
                    print(f"src : {sx},{sy}", src_img[sx * moc_size, sy * moc_size])
                    print(f"tgt : {rx + sx},{ry + sy}", tgt_img[(rx + sx) * moc_size, (ry + sy) * moc_size])
                    print()
            
    print(f"Match Len : {len(match)}")


