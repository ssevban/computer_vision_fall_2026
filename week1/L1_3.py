from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

GAMMA = 2.2


def decode(e):
    return e ** GAMMA


def encode(l):
    return l ** (1.0 / GAMMA)


print("--- 1) siyah + beyaz cifti (slayt s.33) ---")
a, b = 0.0, 1.0
naive = (a + b) / 2
correct = encode((decode(a) + decode(b)) / 2)
print("naif   (kodlu uzayda ortalama): %.4f  ->  8 bit: %3d" % (naive, round(naive * 255)))
print("dogru  (lineer uzayda)        : %.4f  ->  8 bit: %3d" % (correct, round(correct * 255)))
print("sapma                         : %.4f  ->  %d ton" % (correct - naive,
                                                            round(correct * 255) - round(naive * 255)))

W = 512
DELTA = 0.10

base_enc_row = np.linspace(DELTA, 1.0 - DELTA, W)
base_enc_img = np.tile(base_enc_row, (128, 1))
ripple = np.where(np.arange(W) % 2 == 0, DELTA, -DELTA)
enc = base_enc_img + ripple

naive_pair = (enc[:, 0::2] + enc[:, 1::2]) / 2.0
correct_pair = encode((decode(enc[:, 0::2]) + decode(enc[:, 1::2])) / 2.0)
err = (correct_pair - naive_pair) * 255.0

base_enc = base_enc_img[:, 0::2]

print()
print("--- 2) gradyan goruntude bolge bazli hata ---")
print("kurulum: komsu piksel ciftleri kodlu uzayda +-%.2f (8 bitte +-%d ton) fark ediyor;" % (DELTA, round(DELTA * 255)))
print("         her cift yari boyuta indirgeniyor. kirpma (clip) yok.")
print("isaret : pozitif = naif sonuc olmasi gerekenden KOYU")
print()
print("bolge    kodlu taban     ort. hata   maks hata   (8 bit ton)")
bounds = [(0.0, 1 / 3, "koyu"), (1 / 3, 2 / 3, "orta"), (2 / 3, 1.0, "acik")]
for lo, hi, name in bounds:
    m = (base_enc >= lo) & (base_enc < hi)
    print("%-8s %.2f - %.2f       %6.2f      %6.2f" % (name, lo, hi, err[m].mean(), err[m].max()))
print("%-8s %.2f - %.2f       %6.2f      %6.2f" % ("tumu", 0.0, 1.0, err.mean(), err.max()))
print()
print("koyu / acik hata orani: %.1f kat" % (
    err[(base_enc < 1 / 3)].mean() / err[(base_enc >= 2 / 3)].mean()))

print()
print("--- 3) ornek piksel hesabi (koyu bolgeden bir cift) ---")
col = 60
e0, e1 = enc[0, col], enc[0, col + 1]
n = (e0 + e1) / 2
c = encode((decode(e0) + decode(e1)) / 2)
print("dosyadaki (kodlu, sRGB) degerler:")
print("  E0 = %.4f  (8 bit %3d)     E1 = %.4f  (8 bit %3d)" % (e0, round(e0 * 255), e1, round(e1 * 255)))
print()
print("adim 1 - coz (kodlu -> lineer isik):")
print("  L0 = %.4f^%.1f = %.5f" % (e0, GAMMA, decode(e0)))
print("  L1 = %.4f^%.1f = %.5f" % (e1, GAMMA, decode(e1)))
print("adim 2 - lineer uzayda ortala:")
print("  Lort = (%.5f + %.5f)/2 = %.5f" % (decode(e0), decode(e1), (decode(e0) + decode(e1)) / 2))
print("adim 3 - tekrar kodla:")
print("  E = %.5f^(1/%.1f) = %.4f   ->  8 bit %d   [DOGRU]" % (
    (decode(e0) + decode(e1)) / 2, GAMMA, c, round(c * 255)))
print()
print("naif yol (kodlu uzayda dogrudan ortalama):")
print("  (%.4f + %.4f)/2 = %.4f              ->  8 bit %d   [YANLIS]" % (e0, e1, n, round(n * 255)))
print()
print("fark: %.4f  ->  %.2f ton; naif sonuc daha koyu" % (c - n, (c - n) * 255))

fig, ax = plt.subplots(3, 1, figsize=(11, 8))
ax[0].imshow(np.clip(naive_pair, 0, 1), cmap="gray", vmin=0, vmax=1, aspect="auto")
ax[0].set_ylabel("naif")
ax[1].imshow(np.clip(correct_pair, 0, 1), cmap="gray", vmin=0, vmax=1, aspect="auto")
ax[1].set_ylabel("dogru")
im = ax[2].imshow(err, cmap="inferno", aspect="auto")
ax[2].set_ylabel("hata (ton)")
for a_ in ax:
    a_.set_xticks([])
    a_.set_yticks([])
ax[0].set_title("yari boyuta indirme: naif vs dogrusal uzay")
fig.colorbar(im, ax=ax[2], orientation="horizontal", fraction=0.15, pad=0.05)
plt.tight_layout()
plt.savefig(OUT / "07_gamma_ortalama.png", dpi=120)

plt.figure(figsize=(8, 5))
plt.plot(base_enc[0], err[0], lw=1.4)
plt.xlabel("kodlu (sRGB) taban parlaklik")
plt.ylabel("hata (8 bit ton)")
plt.title("hata parlaklikla nasil degisiyor")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "08_hata_egrisi.png", dpi=120)

plt.show()
