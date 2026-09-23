from pathlib import Path

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

HERE = Path(__file__).parent
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

img = np.array(Image.open(HERE / "kodim19.png"), dtype=np.float64)
H, W, _ = img.shape

print("boyut :", img.shape)
print("aralik:", img.min(), "-", img.max())


def bayer_masks(h, w):
    mr = np.zeros((h, w), dtype=bool)
    mg = np.zeros((h, w), dtype=bool)
    mb = np.zeros((h, w), dtype=bool)
    mr[0::2, 0::2] = True
    mg[0::2, 1::2] = True
    mg[1::2, 0::2] = True
    mb[1::2, 1::2] = True
    return mr, mg, mb


MR, MG, MB = bayer_masks(H, W)

raw = np.zeros((H, W), dtype=np.float64)
raw[MR] = img[:, :, 0][MR]
raw[MG] = img[:, :, 1][MG]
raw[MB] = img[:, :, 2][MB]

print()
print("--- mozaikleme ---")
print("R piksel: %7d  (%.1f%%)" % (MR.sum(), 100 * MR.sum() / MR.size))
print("G piksel: %7d  (%.1f%%)" % (MG.sum(), 100 * MG.sum() / MG.size))
print("B piksel: %7d  (%.1f%%)" % (MB.sum(), 100 * MB.sum() / MB.size))
print("orijinal olcum sayisi : %d" % img.size)
print("ham sensor olcum sayisi: %d" % raw.size)
print("kaybedilen             : %.1f%%" % (100 * (1 - raw.size / img.size)))

cfa_rgb = np.zeros_like(img)
cfa_rgb[:, :, 0][MR] = raw[MR]
cfa_rgb[:, :, 1][MG] = raw[MG]
cfa_rgb[:, :, 2][MB] = raw[MB]


K_G = np.array([[0.0, 1.0, 0.0],
                [1.0, 4.0, 1.0],
                [0.0, 1.0, 0.0]]) / 4.0

K_RB = np.array([[1.0, 2.0, 1.0],
                 [2.0, 4.0, 2.0],
                 [1.0, 2.0, 1.0]]) / 4.0


def conv(x, k):
    return cv2.filter2D(x, -1, k, borderType=cv2.BORDER_REFLECT)


def demosaic_bilinear(raw, mr, mg, mb):
    out = np.zeros(raw.shape + (3,), dtype=np.float64)
    out[:, :, 0] = conv(raw * mr, K_RB)
    out[:, :, 1] = conv(raw * mg, K_G)
    out[:, :, 2] = conv(raw * mb, K_RB)
    return out


def psnr(a, b, peak=255.0):
    mse = np.mean((a - b) ** 2)
    return float("inf") if mse == 0 else 10.0 * np.log10(peak ** 2 / mse)


rec = demosaic_bilinear(raw, MR, MG, MB)

print()
print("--- PSNR ---")
for i, name in enumerate(["R", "G", "B"]):
    print("%s : %6.2f dB   (MSE %8.2f)" % (
        name, psnr(img[:, :, i], rec[:, :, i]),
        np.mean((img[:, :, i] - rec[:, :, i]) ** 2)))
print("toplam: %6.2f dB" % psnr(img, rec))

plt.figure(figsize=(6, 9))
plt.imshow(img.astype(np.uint8))
plt.axis("off")
plt.title("orijinal (referans)")
plt.tight_layout()
plt.savefig(OUT / "01_orijinal.png", dpi=120)

fig, ax = plt.subplots(1, 3, figsize=(13, 5))
ax[0].imshow(raw, cmap="gray", vmin=0, vmax=255)
ax[0].set_title("ham sensor (RAW, tek kanal)")
ax[1].imshow(raw[200:216, 200:216], cmap="gray", vmin=0, vmax=255, interpolation="nearest")
ax[1].set_title("RAW 16x16 buyutulmus")
ax[2].imshow(cfa_rgb[200:216, 200:216].astype(np.uint8), interpolation="nearest")
ax[2].set_title("ayni bolge, filtre renkleriyle")
for a in ax:
    a.axis("off")
plt.tight_layout()
plt.savefig(OUT / "02_mozaik.png", dpi=120)

plt.show()
