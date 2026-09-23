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


err = np.abs(img - rec)

print()
print("--- hata dagilimi ---")
for i, name in enumerate(["R", "G", "B"]):
    print("%s : ortalama %5.2f   maks %6.2f" % (name, err[:, :, i].mean(), err[:, :, i].max()))

gray = img.mean(axis=2)
gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
grad = np.hypot(gx, gy)

edge = grad >= np.percentile(grad, 90)
flat = grad <= np.percentile(grad, 50)
err_sum = err.sum(axis=2)

print()
print("--- hata nerede toplaniyor ---")
print("kenar pikselleri (ust %%10 gradyan): ortalama hata %6.2f" % err_sum[edge].mean())
print("duz pikseller    (alt %%50 gradyan): ortalama hata %6.2f" % err_sum[flat].mean())
print("oran                              : %.1f kat" % (err_sum[edge].mean() / err_sum[flat].mean()))

box = cv2.boxFilter(err_sum, -1, (32, 32), normalize=False)
cy, cx = np.unravel_index(np.argmax(box), box.shape)
y0 = int(np.clip(cy - 16, 0, H - 32))
x0 = int(np.clip(cx - 16, 0, W - 32))
print()
print("en bozuk 32x32 bolge: satir %d-%d, sutun %d-%d" % (y0, y0 + 32, x0, x0 + 32))

fig, ax = plt.subplots(1, 3, figsize=(14, 7))
for i, name in enumerate(["R", "G", "B"]):
    im = ax[i].imshow(err[:, :, i], cmap="inferno", vmin=0, vmax=60)
    ax[i].set_title("%s hata haritasi" % name)
    ax[i].axis("off")
fig.colorbar(im, ax=ax, fraction=0.03)
plt.savefig(OUT / "03_hata_haritasi.png", dpi=120, bbox_inches="tight")

crop_o = img[y0:y0 + 32, x0:x0 + 32]
crop_r = rec[y0:y0 + 32, x0:x0 + 32]
fig, ax = plt.subplots(1, 3, figsize=(14, 5))
ax[0].imshow(crop_o.astype(np.uint8), interpolation="nearest")
ax[0].set_title("orijinal")
ax[1].imshow(np.clip(crop_r, 0, 255).astype(np.uint8), interpolation="nearest")
ax[1].set_title("demozaiklenmis (zipper)")
im = ax[2].imshow(np.abs(crop_o - crop_r).sum(axis=2), cmap="inferno", interpolation="nearest")
ax[2].set_title("fark")
for a in ax:
    a.axis("off")
fig.colorbar(im, ax=ax[2], fraction=0.046)
plt.savefig(OUT / "04_zipper.png", dpi=150, bbox_inches="tight")

fig, ax = plt.subplots(1, 2, figsize=(11, 9))
ax[0].imshow(img.astype(np.uint8))
ax[0].set_title("orijinal (referans)")
ax[1].imshow(np.clip(rec, 0, 255).astype(np.uint8))
ax[1].set_title("demozaiklenmis (%.2f dB)" % psnr(img, rec))
for a in ax:
    a.axis("off")
plt.tight_layout()
plt.savefig(OUT / "01_orijinal_vs_geri_kurulmus.png", dpi=120)

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
