from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

W_S = 13.2
N_X = 5472
F_MM = 8.8

s_px = W_S / N_X
f_x = F_MM / s_px

print("--- kamera sabitleri (Cozumlu Ornek 1.1 ile ayni) ---")
print("sensor genisligi  W_s = %.1f mm" % W_S)
print("yatay piksel      N_x = %d px" % N_X)
print("odak uzakligi     f   = %.1f mm" % F_MM)
print()
print("piksel boyutu     s_px = W_s / N_x = %.1f / %d = %.6e mm/px" % (W_S, N_X, s_px))
print("piksel cinsinden  f_x  = f / s_px  = %.1f / %.6e = %.1f px" % (F_MM, s_px, f_x))
print("birim kontrolu    mm / (mm/px) = px  OK")

heights = [60.0, 120.0, 240.0]

print()
print("--- GSD ve serit genisligi ---")
print("GSD    = Z / f_x")
print("serit  = GSD * N_x = Z * W_s / f")
print()
print("   Z (m)      GSD (m/px)   GSD (cm/px)   serit (m)   120 m'ye gore")
for Z in heights:
    gsd = Z / f_x
    swath = gsd * N_X
    ref = (Z / 120.0)
    tag = "referans" if Z == 120.0 else "%.2fx" % ref
    print("   %6.1f     %.6f     %8.2f      %8.1f    %s" % (Z, gsd, gsd * 100, swath, tag))

print()
print("--- capraz dogrulama: gorus acisindan (FOV) ---")
fov = 2 * np.arctan(W_S / (2 * F_MM))
print("FOV_yatay = 2*arctan(W_s / 2f) = 2*arctan(%.1f / %.1f) = %.2f derece" % (W_S, 2 * F_MM, np.degrees(fov)))
for Z in heights:
    swath_fov = 2 * Z * np.tan(fov / 2)
    swath_gsd = (Z / f_x) * N_X
    print("Z=%6.1f m -> FOV'dan %8.1f m | GSD'den %8.1f m | fark %.2e" % (
        Z, swath_fov, swath_gsd, abs(swath_fov - swath_gsd)))

print()
print("--- dogrusallik ---")
print("GSD = Z / f_x ifadesinde f_x kameranin sabiti; tek degisken Z.")
print("Z iki katina cikinca GSD ve serit de tam iki katina cikiyor:")
g60, g120, g240 = [Z / f_x for Z in heights]
print("  GSD(120)/GSD(60)  = %.4f" % (g120 / g60))
print("  GSD(240)/GSD(120) = %.4f" % (g240 / g120))
print()
print("bu kamera icin serit = Z * W_s / f = Z * %.1f / %.1f = %.2f * Z" % (W_S, F_MM, W_S / F_MM))

zz = np.linspace(20, 400, 300)
fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
ax[0].plot(zz, (zz / f_x) * 100, lw=1.6)
ax[0].scatter(heights, [(Z / f_x) * 100 for Z in heights], color="crimson", zorder=3)
for Z in heights:
    ax[0].annotate("%.2f cm/px" % ((Z / f_x) * 100), (Z, (Z / f_x) * 100),
                   textcoords="offset points", xytext=(6, -10), fontsize=9)
ax[0].set_xlabel("ucus yuksekligi Z (m)")
ax[0].set_ylabel("GSD (cm/px)")
ax[0].set_title("GSD = Z / f_x")
ax[0].grid(alpha=0.3)

ax[1].plot(zz, (zz / f_x) * N_X, lw=1.6, color="seagreen")
ax[1].scatter(heights, [(Z / f_x) * N_X for Z in heights], color="crimson", zorder=3)
for Z in heights:
    ax[1].annotate("%.0f m" % ((Z / f_x) * N_X), (Z, (Z / f_x) * N_X),
                   textcoords="offset points", xytext=(6, -10), fontsize=9)
ax[1].set_xlabel("ucus yuksekligi Z (m)")
ax[1].set_ylabel("serit genisligi (m)")
ax[1].set_title("serit = 1.5 * Z")
ax[1].grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "09_gsd.png", dpi=120)
plt.show()
