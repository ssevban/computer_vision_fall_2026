from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

N = 200_000
ramp = np.linspace(0.0, 1.0, N, endpoint=False)


def quantize(x, bits):
    levels = 2 ** bits
    idx = np.clip(np.floor(x * levels), 0, levels - 1)
    return (idx + 0.5) / levels


def snr_db(sig, q):
    err = sig - q
    return 10.0 * np.log10(np.var(sig) / np.mean(err ** 2))


bits = np.arange(2, 9)
measured = np.array([snr_db(ramp, quantize(ramp, b)) for b in bits])
theory = 6.02 * bits

print("--- nicemleme ve SNR ---")
print(" B   seviye      delta     olculen SNR   teori 6.02B    fark")
for b, m, t in zip(bits, measured, theory):
    print("%2d   %6d   %.3e    %8.2f dB    %8.2f dB   %+6.2f" %
          (b, 2 ** b, 1 / 2 ** b, m, t, m - t))

slope, intercept = np.polyfit(bits, measured, 1)
print()
print("dogrusal uyum: SNR = %.3f * B + %.3f" % (slope, intercept))
print("olculen egim : %.3f dB/bit" % slope)
print("teorik egim  : 6.021 dB/bit   (20*log10(2))")
print("sapma        : %.2f%%" % (100 * abs(slope - 6.0206) / 6.0206))

fig, ax = plt.subplots(1, 2, figsize=(13, 5))
ax[0].plot(bits, measured, "o-", label="olculen")
ax[0].plot(bits, theory, "--", label="teori: 6.02 B")
ax[0].set_xlabel("bit derinligi B")
ax[0].set_ylabel("SNR (dB)")
ax[0].set_title("SNR - B  (egim = %.2f dB/bit)" % slope)
ax[0].grid(alpha=0.3)
ax[0].legend()

for b in [2, 3, 8]:
    ax[1].plot(ramp[::200], quantize(ramp, b)[::200], label="B=%d" % b)
ax[1].plot(ramp[::200], ramp[::200], "k--", lw=0.8, label="surekli")
ax[1].set_xlabel("giris")
ax[1].set_ylabel("nicemlenmis cikis")
ax[1].set_title("nicemleme merdiveni")
ax[1].grid(alpha=0.3)
ax[1].legend()
plt.tight_layout()
plt.savefig(OUT / "05_snr_b.png", dpi=120)

ramp2d = np.tile(np.linspace(0, 1, 512), (160, 1))
fig, ax = plt.subplots(4, 1, figsize=(11, 7))
for a, b in zip(ax, [2, 3, 4, 8]):
    a.imshow(quantize(ramp2d, b), cmap="gray", vmin=0, vmax=1, aspect="auto")
    a.set_ylabel("B=%d" % b)
    a.set_xticks([])
    a.set_yticks([])
ax[0].set_title("bant olusumu (banding)")
plt.tight_layout()
plt.savefig(OUT / "06_banding.png", dpi=120)

plt.show()
