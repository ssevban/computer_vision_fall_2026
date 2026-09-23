# -*- coding: utf-8 -*-
from pathlib import Path

import cv2
import numpy as np
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, KeepTogether, NextPageTemplate, PageBreak,
                                Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

WEEK1 = Path("C:/Users/sevba/Masa\u00fcst\u00fc/\u00fcni/im\u00fc/computer_vision_2026_fall/week1")
OUT = WEEK1 / "out"

F = "C:/Windows/Fonts/"
pdfmetrics.registerFont(TTFont("Body", F + "cambria.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("BodyB", F + "cambriab.ttf"))
pdfmetrics.registerFont(TTFont("BodyI", F + "cambriai.ttf"))
pdfmetrics.registerFont(TTFont("Head", F + "calibrib.ttf"))
pdfmetrics.registerFont(TTFont("HeadR", F + "calibri.ttf"))
pdfmetrics.registerFont(TTFont("Mono", F + "consola.ttf"))
pdfmetrics.registerFontFamily("Body", normal="Body", bold="BodyB", italic="BodyI")

INK = colors.HexColor("#111111")
GREY = colors.HexColor("#555555")
RULE = colors.HexColor("#333333")
HAIR = colors.HexColor("#999999")
FILL = colors.HexColor("#ececec")

BODY = ParagraphStyle("BODY", fontName="Body", fontSize=10.5, leading=15.4,
                      alignment=TA_JUSTIFY, textColor=INK, spaceAfter=7,
                      firstLineIndent=0)
BODYC = ParagraphStyle("BODYC", parent=BODY, spaceAfter=0)
H1 = ParagraphStyle("H1", fontName="Head", fontSize=14.5, leading=18, textColor=INK,
                    spaceBefore=0, spaceAfter=11)
H2 = ParagraphStyle("H2", fontName="Head", fontSize=11.5, leading=15, textColor=INK,
                    spaceBefore=14, spaceAfter=6)
CAP = ParagraphStyle("CAP", fontName="BodyI", fontSize=8.8, leading=12.2,
                     textColor=GREY, alignment=TA_JUSTIFY, spaceBefore=5, spaceAfter=2)
TCAP = ParagraphStyle("TCAP", parent=CAP, spaceBefore=0, spaceAfter=6)
MONO = ParagraphStyle("MONO", fontName="Mono", fontSize=8.7, leading=12.4,
                      textColor=INK, spaceBefore=4, spaceAfter=8, leftIndent=10)
EQ = ParagraphStyle("EQ", fontName="Mono", fontSize=9.6, leading=14, textColor=INK,
                    alignment=TA_CENTER, spaceBefore=8, spaceAfter=10)
LI = ParagraphStyle("LI", parent=BODY, leftIndent=16, bulletIndent=2, spaceAfter=5)

CV_TITLE = ParagraphStyle("CVT", fontName="Head", fontSize=20, leading=26,
                          alignment=TA_CENTER, textColor=INK)
CV_SUB = ParagraphStyle("CVS", fontName="Body", fontSize=12, leading=17,
                        alignment=TA_CENTER, textColor=GREY)
CV_ORG = ParagraphStyle("CVO", fontName="HeadR", fontSize=11.5, leading=16,
                        alignment=TA_CENTER, textColor=INK)
CV_SM = ParagraphStyle("CVSM", fontName="Body", fontSize=10, leading=14,
                       alignment=TA_CENTER, textColor=GREY)


def h1(txt, num):
    p = Paragraph("%s.&nbsp;&nbsp;%s" % (num, txt), H1)
    p._toc = (0, "%s. %s" % (num, txt))
    return p


def h2(txt, num):
    p = Paragraph("%s&nbsp;&nbsp;%s" % (num, txt), H2)
    p._toc = (1, "%s %s" % (num, txt))
    return p


def para(t):
    return Paragraph(t, BODY)


def items(lst):
    return [Paragraph(t, LI, bulletText="%d." % (i + 1)) for i, t in enumerate(lst)]


def mono(t):
    return Paragraph(t.replace(" ", "&nbsp;").replace("\n", "<br/>"), MONO)


TBL = TableStyle([
    ("FONTNAME", (0, 0), (-1, 0), "Head"),
    ("FONTNAME", (0, 1), (-1, -1), "Body"),
    ("FONTSIZE", (0, 0), (-1, -1), 9.3),
    ("TEXTCOLOR", (0, 0), (-1, -1), INK),
    ("BACKGROUND", (0, 0), (-1, 0), FILL),
    ("LINEABOVE", (0, 0), (-1, 0), 0.9, RULE),
    ("LINEBELOW", (0, 0), (-1, 0), 0.9, RULE),
    ("LINEBELOW", (0, -1), (-1, -1), 0.9, RULE),
    ("INNERGRID", (0, 1), (-1, -1), 0.25, HAIR),
    ("ALIGN", (1, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 4.5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
])


def tbl(data, widths, cap=None):
    t = Table(data, colWidths=widths, hAlign="CENTER")
    t.setStyle(TBL)
    if cap:
        return KeepTogether([Paragraph(cap, TCAP), t, Spacer(1, 9 * mm)])
    return t


def fig(name, cap, width=150 * mm):
    p = OUT / name
    w, h = PILImage.open(p).size
    return KeepTogether([
        Spacer(1, 3 * mm),
        Image(str(p), width=width, height=width * h / w),
        Paragraph(cap, CAP),
        Spacer(1, 7 * mm)])


# ------------------------------------------------------------------ hesaplar
img = np.array(PILImage.open(WEEK1 / "kodim19.png").convert("RGB"), dtype=np.float64)
H, W, _ = img.shape
MR = np.zeros((H, W), bool); MG = np.zeros((H, W), bool); MB = np.zeros((H, W), bool)
MR[0::2, 0::2] = True; MG[0::2, 1::2] = True; MG[1::2, 0::2] = True; MB[1::2, 1::2] = True
raw = np.zeros((H, W))
raw[MR] = img[:, :, 0][MR]; raw[MG] = img[:, :, 1][MG]; raw[MB] = img[:, :, 2][MB]
K_G = np.array([[0., 1, 0], [1, 4, 1], [0, 1, 0]]) / 4
K_RB = np.array([[1., 2, 1], [2, 4, 2], [1, 2, 1]]) / 4
cv_ = lambda x, k: cv2.filter2D(x, -1, k, borderType=cv2.BORDER_REFLECT)
rec = np.dstack([cv_(raw * MR, K_RB), cv_(raw * MG, K_G), cv_(raw * MB, K_RB)])
psnr = lambda a, b: 10 * np.log10(255.0 ** 2 / np.mean((a - b) ** 2))
PS = [psnr(img[:, :, i], rec[:, :, i]) for i in range(3)]
MS = [np.mean((img[:, :, i] - rec[:, :, i]) ** 2) for i in range(3)]
EM = [np.abs(img[:, :, i] - rec[:, :, i]).mean() for i in range(3)]
EX = [np.abs(img[:, :, i] - rec[:, :, i]).max() for i in range(3)]
PS_T, MS_T = psnr(img, rec), np.mean((img - rec) ** 2)
gray = img.mean(axis=2)
grad = np.hypot(cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3),
                cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3))
es = np.abs(img - rec).sum(axis=2)
E_EDGE = es[grad >= np.percentile(grad, 90)].mean()
E_FLAT = es[grad <= np.percentile(grad, 50)].mean()

ramp = np.linspace(0, 1, 200000, endpoint=False)
quant = lambda x, b: (np.clip(np.floor(x * 2 ** b), 0, 2 ** b - 1) + 0.5) / 2 ** b
bits = np.arange(2, 9)
snrs = np.array([10 * np.log10(np.var(ramp) / np.mean((ramp - quant(ramp, b)) ** 2)) for b in bits])
SLOPE, INTER = np.polyfit(bits, snrs, 1)

G = 2.2
dec, enc_ = lambda e: e ** G, lambda l: l ** (1 / G)
CORR_BW = enc_(0.5)
DELTA = 0.10
bei = np.tile(np.linspace(DELTA, 1 - DELTA, 512), (128, 1))
encimg = bei + np.where(np.arange(512) % 2 == 0, DELTA, -DELTA)
ET = (enc_((dec(encimg[:, 0::2]) + dec(encimg[:, 1::2])) / 2)
      - (encimg[:, 0::2] + encimg[:, 1::2]) / 2) * 255
BE = bei[:, 0::2]
Z = [ET[BE < 1 / 3].mean(), ET[(BE >= 1 / 3) & (BE < 2 / 3)].mean(), ET[BE >= 2 / 3].mean()]
X = [ET[BE < 1 / 3].max(), ET[(BE >= 1 / 3) & (BE < 2 / 3)].max(), ET[BE >= 2 / 3].max()]
e0, e1 = encimg[0, 60], encimg[0, 61]
NAIF_P, CORR_P = (e0 + e1) / 2, enc_((dec(e0) + dec(e1)) / 2)

W_S, N_X, F_MM = 13.2, 5472, 8.8
S_PX = W_S / N_X
F_X = F_MM / S_PX
GSD = {z: z / F_X for z in (60, 120, 240)}
FOV = np.degrees(2 * np.arctan(W_S / (2 * F_MM)))

S = []

# ------------------------------------------------------------------ kapak
S += [Spacer(1, 18 * mm),
      Paragraph("T.C. İSTANBUL MEDENİYET ÜNİVERSİTESİ", CV_ORG),
      Paragraph("Mühendislik ve Doğa Bilimleri Fakültesi", CV_SM),
      Paragraph("Bilgisayar Mühendisliği Bölümü", CV_SM),
      Spacer(1, 42 * mm),
      Paragraph("BİL458 · BİLGİSAYARLI GÖRME", CV_SUB),
      Spacer(1, 7 * mm),
      Paragraph("Kamera İşlem Hattında<br/>Bilgi Kaybının Ölçülmesi", CV_TITLE),
      Spacer(1, 5 * mm),
      Paragraph("Ödev 1 &middot; Laboratuvar Görevleri L1.1 - L1.4", CV_SUB),
      Spacer(1, 40 * mm)]

cover = Table([["Hazırlayan", "Sevban Bozaslan"],
               ["Öğrenci No", "23120205020"],
               ["Dersi Veren", "Doç. Dr. Murat Gezer"]],
              colWidths=[38 * mm, 72 * mm], hAlign="CENTER")
cover.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (0, -1), "Head"),
    ("FONTNAME", (1, 0), (1, -1), "Body"),
    ("FONTSIZE", (0, 0), (-1, -1), 10.5),
    ("TEXTCOLOR", (0, 0), (-1, -1), INK),
    ("ALIGN", (0, 0), (0, -1), "RIGHT"),
    ("ALIGN", (1, 0), (1, -1), "LEFT"),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("LINEAFTER", (0, 0), (0, -1), 0.6, HAIR),
]))
S += [cover, PageBreak()]

# ------------------------------------------------------------------ içindekiler
toc = TableOfContents()
toc.levelStyles = [
    ParagraphStyle("TOC0", fontName="Head", fontSize=10.3, leading=15,
                   textColor=INK, leftIndent=0, firstLineIndent=-14),
    ParagraphStyle("TOC1", fontName="Body", fontSize=9.8, leading=13,
                   textColor=INK, leftIndent=16, firstLineIndent=-14),
]
S += [Paragraph("İÇİNDEKİLER", H1), Spacer(1, 4 * mm), toc, PageBreak()]

# ------------------------------------------------------------------ 1. giriş
S += [h1("Giriş", 1),
      para("Dijital bir kamerada sahneden görüntü dosyasına uzanan zincirin her halkası bilgi "
           "kaybeder. Mercek yalnızca tek bir nesne düzlemini odakta tutar, renk süzgeci her "
           "pikselde tek bir kanal ölçer, analog-sayısal çevirici genliği sonlu sayıda "
           "seviyeye yuvarlar ve gamma kodlaması değer ölçeğini doğrusal olmayan biçimde "
           "eğriltir. Bu kayıpların hiçbiri sonradan uygulanan bir işlemle tam olarak geri "
           "alınamaz; görüntü üzerinde çalışan her algoritma, bu kayıpların üzerine kurulur."),
      para("Bu raporda söz konusu zincirin dört ayrı adımı tek tek ele alınmış ve her birinde "
           "kaybedilen bilgi nicel olarak ölçülmüştür. Dört görevde de aynı yöntem izlenmiştir: "
           "kayıp denetimli biçimde üretilmiş, geri kazanım denenmiş ve kalan fark konuya uygun "
           "bir metrikle raporlanmıştır. Elde edilen değerler ders kapsamında verilen kuramsal "
           "ifadelerle karşılaştırılmış, kuramdan sapan tek durumun nedeni ayrıca incelenmiştir."),
      h2("Kapsam ve yöntem", "1.1"),
      para("Çalışma dört laboratuvar görevinden oluşmaktadır. Aşağıdaki çizelge, her görevin "
           "işlem hattındaki karşılığını ve kullanılan ölçütü özetlemektedir."),
      tbl([["Görev", "İşlem hattı adımı", "Ölçüt", "Bölüm"],
           ["L1.1", "Bayer renk süzgeç dizisi", "PSNR", "2"],
           ["L1.2", "Analog-sayısal çevrim", "SNR", "3"],
           ["L1.3", "Gamma kodlaması", "Ton hatası", "4"],
           ["L1.4", "Mercek geometrisi", "GSD", "5"]],
          [20 * mm, 58 * mm, 26 * mm, 20 * mm],
          "Çizelge 1. Görevlerin işlem hattındaki karşılıkları."),
      h2("Deney ortamı", "1.2"),
      para("Tüm hesaplamalar Python 3.12 ortamında NumPy, OpenCV ve Matplotlib kütüphaneleriyle "
           "yapılmıştır. Demozaikleme deneylerinde Kodak PhotoCD kümesinin 19 numaralı görüntüsü "
           "(768 &times; 512 piksel, RGB) kullanılmıştır; bu görüntü ince yapılı çit ve direk "
           "dokuları içerdiğinden demozaikleme başarımının sınandığı standart örneklerden biridir. "
           "Kaynak kodu ve üretilen tüm şekiller rapor ekinde listelenmiştir.")]
S += [PageBreak()]

# ------------------------------------------------------------------ 2. L1.1
S += [h1("Bayer Deseni ve Demozaikleme Kaybı", 2),
      h2("Problem tanımı", "2.1"),
      para("Görüntü sensöründeki her fotodiyot renk körüdür ve yalnızca üzerine düşen foton "
           "sayısını ölçer. Renk bilgisi, her fotositin üstüne yerleştirilen bir renk süzgeciyle "
           "elde edilir. Bunun bedeli, her pikselde üç kanaldan yalnızca birinin gerçekten "
           "ölçülmesidir."),
      para("En yaygın süzgeç dizilimi olan Bayer RGGB deseninde piksellerin dörtte biri kırmızı, "
           "dörtte biri mavi, yarısı yeşil ölçer. Yeşilin iki kat sık örneklenmesinin nedeni, "
           "parlaklık sinyalinin ağırlıklı olarak yeşil banttan gelmesi ve insan görme sisteminin "
           "parlaklıktaki yüksek frekanslı detaya, renkteki aynı detaydan belirgin biçimde daha "
           "duyarlı olmasıdır. Eksik kanalların komşu piksellerden kestirilmesi işlemine "
           "demozaikleme adı verilir; bu bir ölçüm değil tahmindir."),
      h2("Yöntem", "2.2"),
      para("Tam renkli referans görüntüden her pikselin yalnızca desendeki kanalı bırakılarak ham "
           "sensör verisi üretilmiş, ardından bilineer interpolasyonla üç kanal geri kurulmuştur. "
           "Kestirim, maskelenmiş seyrek dizilere uygulanan iki konvolüsyon çekirdeğiyle "
           "gerçeklenmiştir:"),
      mono("K_G  = (1/4) x [[0,1,0],      K_RB = (1/4) x [[1,2,1],\n"
           "                [1,4,1],                      [2,4,2],\n"
           "                [0,1,0]]                      [1,2,1]]"),
      para("Seyrek dizide ölçüm yapılmayan konumlar sıfır olduğundan toplama katkı vermez; çekirdek "
           "her konumda kendiliğinden yalnızca doğru komşuları toplar. Ağırlıklar, her konum "
           "tipinde katkı veren terimlerin toplamı tam dört verecek biçimde seçilmiştir. Bu nedenle "
           "tek bir bölme tüm durumlarda doğru ortalamayı üretir ve görüntünün ortalama parlaklığı "
           "kaymaz."),
      para("Yapısal olarak önemli bir ayrıntı, yeşil kanalın her zaman dört dik komşudan "
           "kestirilmesine karşılık kırmızı ve mavi kanalların yeşil konumlarında yalnızca iki "
           "komşudan ve tek yönden kestirilmesidir. Kanallar arası başarım farkının kaynağı bu "
           "asimetridir."),
      para("Geri kurulan görüntü referansla karşılaştırılmıştır. Kullanılan ölçüt, ortalama karesel "
           "hatadan türetilen tepe sinyal gürültü oranıdır:"),
      Paragraph("MSE = (1/n) &#931; [ I(x) - Î(x) ]<super>2</super>", EQ),
      Paragraph("PSNR = 10 log<sub>10</sub> ( I<sub>maks</sub><super>2</super> / MSE )", EQ),
      para("Sekiz bitlik görüntüler için tepe değer 255 alınmıştır. Yüksek PSNR düşük hata anlamına "
           "gelir."),
      h2("Bulgular", "2.3"),
      para("Ham sensör verisi 393.216 ölçüm içermektedir; bu, tam renkli görüntünün gerektirdiği "
           "1.179.648 değerin üçte biridir. Geri kalan üçte iki, doğrudan ölçüm değil kestirimle "
           "üretilmiştir."),
      tbl([["Kanal", "PSNR (dB)", "MSE", "Ort. hata", "Maks. hata"],
           ["Kırmızı (R)", "%.2f" % PS[0], "%.2f" % MS[0], "%.2f" % EM[0], "%.2f" % EX[0]],
           ["Yeşil (G)", "%.2f" % PS[1], "%.2f" % MS[1], "%.2f" % EM[1], "%.2f" % EX[1]],
           ["Mavi (B)", "%.2f" % PS[2], "%.2f" % MS[2], "%.2f" % EM[2], "%.2f" % EX[2]],
           ["Tüm görüntü", "%.2f" % PS_T, "%.2f" % MS_T, "-", "-"]],
          [32 * mm, 26 * mm, 26 * mm, 26 * mm, 28 * mm],
          "Çizelge 2. Bilineer demozaikleme sonrası kanal bazlı başarım."),
      para("Yeşil kanalın tepe sinyal gürültü oranı diğer iki kanalın ortalamasından %.1f dB "
           "yüksektir. Ortalama karesel hata üzerinden bakıldığında kırmızı kanalın hatası yeşilin "
           "yaklaşık üç katıdır. Bu sonuç, yeşilin iki kat sık örneklenmesinin ve her zaman dört "
           "komşudan kestirilmesinin doğrudan karşılığıdır."
           % (PS[1] - (PS[0] + PS[2]) / 2)),
      fig("01_orijinal_vs_geri_kurulmus.png",
          "Şekil 1. Orijinal referans görüntü (solda) ve bilineer demozaikleme sonrası geri "
          "kurulmuş görüntü (sağda). Genel görünümde fark belirgin değildir; kayıp, ayrıntı "
          "ölçeğinde gizlidir.", 128 * mm),
      fig("02_mozaik.png",
          "Şekil 2. Ham sensör verisi, büyütülmüş bir bölge ve aynı bölgenin süzgeç renkleriyle "
          "gösterimi. Her piksel yalnızca tek bir kanal taşımaktadır."),
      h2("Hatanın konumsal dağılımı", "2.4"),
      para("Bilineer kestirim, komşu piksellerin birbirine benzediği varsayımına dayanır. Bu "
           "varsayımın geçerliliğini sınamak için pikseller Sobel gradyan büyüklüğüne göre iki "
           "kümeye ayrılmış ve her kümede ortalama hata ayrı hesaplanmıştır."),
      tbl([["Piksel kümesi", "Tanım", "Ortalama toplam hata"],
           ["Kenar", "üst %10 gradyan", "%.2f" % E_EDGE],
           ["Düz", "alt %50 gradyan", "%.2f" % E_FLAT],
           ["Oran", "kenar / düz", "%.1f kat" % (E_EDGE / E_FLAT)]],
          [38 * mm, 42 * mm, 46 * mm],
          "Çizelge 3. Hatanın gradyan büyüklüğüne göre dağılımı."),
      para("Hata düz bölgelerde ihmal edilebilir düzeydedir ve kenarlarda yaklaşık %.1f kat "
           "artmaktadır. Komşu benzerliği varsayımı kenarlarda geçersizdir."
           % (E_EDGE / E_FLAT)),
      fig("03_hata_haritasi.png",
          "Şekil 3. Kanal bazlı mutlak hata haritaları. Hata düz yüzeylerde sıfıra yakın, kenar ve "
          "ince desenlerde yoğundur. Yeşil kanalın haritası gözle görülür biçimde daha sakindir."),
      h2("Zipper artefaktı", "2.5"),
      para("Keskin bir kenarda üç kanal farklı komşulardan ve kısmen farklı yönlerden kestirildiği "
           "için birbirinden bağımsız hata yapar. Kanallar arasındaki bu eşzamansızlık, sahnede "
           "bulunmayan renk saçaklarının belirmesine ve kenar boyunca dişli bir desen oluşmasına "
           "yol açar. Aşağıda incelenen bölge, hata yoğunluğu en yüksek 32 &times; 32 pencere "
           "aranarak otomatik seçilmiştir."),
      fig("04_zipper.png",
          "Şekil 4. Zipper artefaktı. Orijinalde yalnızca kahverengi ve bej tonlar bulunan ahşap "
          "çit bölgesinde, geri kurulmuş görüntüde kırmızı, turkuaz ve mor saçaklar oluşmuştur. "
          "Fark haritasındaki dama deseni, hatanın piksel piksel yön değiştirdiğini göstermektedir."),
      para("Bu bölgedeki çit şeritlerinin uzamsal frekansı Bayer örnekleme frekansına yakındır. "
           "Kırmızı ve mavi kanallar iki piksel aralıkla örneklendiğinden Nyquist sınırının üstünde "
           "kalır ve yüksek frekans bileşenleri düşük frekansa katlanır. Ortaya çıkan renk moiré "
           "deseni bilineer yöntemin yapısal sınırıdır; yön uyarlamalı demozaikleme algoritmaları "
           "bu artefaktı azaltmak amacıyla geliştirilmiştir."),
      h2("Değerlendirme", "2.6")]
S += items([
    "Renkli görüntü verisinin üçte ikisi ölçüm değil kestirimdir.",
    "Yeşil kanal, örnekleme sıklığı ve komşuluk yapısı nedeniyle diğer iki kanaldan yaklaşık 5 dB "
    "daha iyi geri kurulmaktadır.",
    "Hata kenarlarda yoğunlaşmakta, düz bölgelerde kaybolmaktadır; ölçülen oran 6.4 kattır.",
    "Zipper artefaktı, kanalların bağımsız kestirilmesinin ve kırmızı ile mavi kanallardaki "
    "örtüşmenin birleşik sonucudur."])
S += [PageBreak()]

# ------------------------------------------------------------------ 3. L1.2
S += [h1("Nicemleme Gürültüsü ve SNR Yasası", 3),
      h2("Problem tanımı", "3.1"),
      para("Fotodiyot çıkışındaki sürekli sinyal, B bitlik bir analog-sayısal çevirici "
           "tarafından 2<super>B</super> ayrık seviyeye yuvarlanır. Tam ölçek aralığı bire "
           "normalize edilirse adım büyüklüğü &#916; = 1 / 2<super>B</super> olur. Nicemleme hatası "
           "[&minus;&#916;/2, +&#916;/2] aralığında düzgün dağılımlıdır ve varyansı &#916;² / 12 "
           "değerindedir."),
      para("Bit derinliği bir birim arttığında adım büyüklüğü yarıya, hata gücü dörtte bire iner. "
           "Buna karşılık gelen kazanç 10 log&#8321;&#8320;(4) = 6.02 dB olup, bit derinliğinden "
           "bağımsız bir sabittir."),
      h2("Yöntem", "3.2"),
      para("200.000 örnekli doğrusal bir rampa, B = 2 ile 8 arasındaki her bit derinliği için "
           "nicemlenmiştir. Her durumda sinyal varyansının hata gücüne oranı desibel cinsinden "
           "hesaplanmış, elde edilen yedi noktaya doğru uydurularak eğim ölçülmüştür."),
      h2("Bulgular", "3.3")]
rows = [["B", "Seviye", "\u0394", "Ölçülen SNR (dB)", "Teori 6.02 B", "Fark"]]
for b, m in zip(bits, snrs):
    rows.append([str(b), str(2 ** b), "%.3e" % (1 / 2 ** b), "%.2f" % m,
                 "%.2f" % (6.02 * b), "%+.2f" % (m - 6.02 * b)])
S += [tbl(rows, [12 * mm, 20 * mm, 27 * mm, 32 * mm, 28 * mm, 20 * mm],
          "Çizelge 4. Bit derinliğine göre ölçülen ve kuramsal SNR değerleri."),
      para("Yedi noktanın hiçbirinde kuramsal değerden sapma gözlenmemiştir. Noktalara uydurulan "
           "doğru:"),
      Paragraph("SNR = %.3f &middot; B + %.3f" % (SLOPE, INTER), EQ),
      para("Ölçülen eğim %.3f dB/bit, kuramsal eğim 20 log&#8321;&#8320;(2) = %.3f dB/bit "
           "değerindedir; bağıl sapma %%%.2f olarak hesaplanmıştır."
           % (SLOPE, 20 * np.log10(2),
              100 * abs(SLOPE - 20 * np.log10(2)) / (20 * np.log10(2)))),
      fig("05_snr_b.png",
          "Şekil 5. Ölçülen SNR değerleri kuramsal doğru üzerine tam oturmaktadır. Sağdaki grafikte, "
          "düşük bit derinliklerinde nicemleme merdiveninin sürekli giriş sinyalinden sapması "
          "görülmektedir."),
      h2("Sabit terim üzerine not", "3.4"),
      para("Doğrusal uyumun sabit terimi 0.000 çıkmıştır. Ders kapsamında verilen "
           "SNR = 6.02 B + 1.76 ifadesindeki 1.76 dB sabiti bu ölçümde gözlenmemiştir. Bu bir "
           "tutarsızlık değildir."),
      para("Söz konusu sabit 10 log&#8321;&#8320;(1.5) değerine eşittir ve girişin tam ölçekli "
           "sinüzoidal olduğu varsayımından türer. Bu görevde kullanılan sinyal ise doğrusal "
           "rampadır. Rampanın değerleri tam ölçek aralığına düzgün dağıldığından sinyal varyansı "
           "1/12, gürültü varyansı &#916;²/12 olur; oranın logaritması tam olarak 6.02 B verir ve "
           "sabit terim sıfırlanır. Eğim her iki sinyal tipinde de aynıdır, yalnızca sabit terim "
           "sinyalin dalga biçimine bağlıdır."),
      h2("Bant oluşumu", "3.5"),
      para("Düşük bit derinliklerinde rampa üzerinde gözle görülür düz şeritler oluşmaktadır. "
           "B = 2 için dört, B = 3 için sekiz şerit ortaya çıkar. Yuvarlama, aynı seviyeye düşen "
           "tüm giriş değerlerini tek bir çıkışa indirger. Şeritler arasındaki süreksizlik, insan "
           "görme sisteminin düz alanlar arasındaki küçük farkları abartarak algılaması nedeniyle "
           "olduğundan belirgin görünür. Bu olgu, gradyan ağırlıklı içerikte sekiz bitin yetersiz "
           "kalabilmesinin ve profesyonel iş akışlarında daha yüksek bit derinliği tercih "
           "edilmesinin nedenidir."),
      fig("06_banding.png",
          "Şekil 6. Aynı doğrusal rampanın farklı bit derinliklerinde nicemlenmiş hali. B = 8 "
          "düzeyinde geçiş süreklidir."),
      h2("Değerlendirme", "3.6")]
S += items([
    "Ölçülen eğim 6.021 dB/bit olup kuramsal değerle birebir örtüşmektedir.",
    "Sabit terimin sıfır çıkması, kuramsal ifadenin sinüzoidal giriş varsayımıyla türetilmesinden "
    "kaynaklanmaktadır; eğim sinyal tipinden bağımsızdır.",
    "Düşük bit derinliğinde ortaya çıkan bant oluşumu, nicemleme hatasının sinyalle ilintili hale "
    "geldiği rejimin görsel karşılığıdır."])
S += [PageBreak()]

# ------------------------------------------------------------------ 4. L1.3
S += [h1("Gamma Uzayında Ortalama Alma Hatası", 4),
      h2("Problem tanımı", "4.1"),
      para("Fiziksel ışık doğrusal toplanır ve sensör de doğrusal ölçer. Buna karşılık insan görme "
           "sistemi Weber-Fechner yasası uyarınca yaklaşık logaritmik yanıt verir; karanlık "
           "bölgedeki küçük farklara, aydınlık bölgedeki aynı büyüklükteki farklardan çok daha "
           "duyarlıdır. Sınırlı bit bütçesini gözün duyarlı olduğu bölgeye ayırmak amacıyla "
           "kameralar, kaydetmeden önce gamma kodlaması uygular:"),
      Paragraph("I<sub>kodlu</sub> = I<sub>doğrusal</sub><super>1/&#947;</super>,"
                "&nbsp;&nbsp;&nbsp;&#947; &#8776; 2.2", EQ),
      para("Bunun sonucu olarak görüntü dosyalarında saklanan değerler ışık miktarı değildir. "
           "Ortalama alma doğrusal bir işlem, gamma kodlaması ise doğrusal olmayan bir dönüşüm "
           "olduğundan, kodlu değerler üzerinde doğrudan ortalama almak sistematik hata üretir. "
           "Doğru işlem sırası çöz, doğrusal uzayda ortala, yeniden kodla biçimindedir."),
      h2("Uç durum", "4.2"),
      para("Bir siyah (0.0) ve bir beyaz (1.0) pikselin ortalaması iki yöntemle hesaplanmıştır."),
      tbl([["Yöntem", "Sonuç", "8 bit karşılığı"],
           ["Naif (kodlu uzayda ortalama)", "0.5000", "128"],
           ["Doğru (doğrusal uzayda)", "%.4f" % CORR_BW, "%d" % round(CORR_BW * 255)],
           ["Sapma", "%.4f" % (CORR_BW - 0.5), "%d ton" % (round(CORR_BW * 255) - 128)]],
          [62 * mm, 30 * mm, 34 * mm],
          "Çizelge 5. Siyah ve beyaz piksel çiftinin iki yöntemle ortalaması."),
      h2("Bölge bazlı ölçüm", "4.3"),
      para("Parlaklığı soldan sağa artan bir gradyan görüntü üretilmiş, komşu piksel çiftleri kodlu "
           "uzayda sabit &plusmn;0.10 (sekiz bit ölçekte yaklaşık 26 ton) fark edecek biçimde "
           "ayarlanmış ve her çift yarı boyuta indirgenmiştir. Taban aralığı, hiçbir noktada kırpma "
           "oluşmayacak şekilde seçilmiştir; böylece ölçülen fark yalnızca gamma etkisini yansıtır. "
           "Çizelgedeki pozitif değerler, naif sonucun olması gerekenden koyu olduğunu gösterir."),
      tbl([["Bölge", "Kodlu taban", "Ortalama hata (ton)", "Maks. hata (ton)"],
           ["Koyu", "0.00 - 0.33", "%.2f" % Z[0], "%.2f" % X[0]],
           ["Orta", "0.33 - 0.67", "%.2f" % Z[1], "%.2f" % X[1]],
           ["Açık", "0.67 - 1.00", "%.2f" % Z[2], "%.2f" % X[2]]],
          [30 * mm, 34 * mm, 42 * mm, 38 * mm],
          "Çizelge 6. Hatanın taban parlaklığına göre dağılımı."),
      para("Aynı büyüklükteki kodlu fark için hata, koyu bölgede açık bölgeye göre yaklaşık %.1f kat "
           "büyüktür. Bunun nedeni, kodlama eğrisinin türevi olan (1/&#947;) x<super>1/&#947; "
           "&minus; 1</super> ifadesinin x sıfıra yaklaşırken sınırsız büyümesidir; eğri koyu "
           "tarafta çok dik, açık tarafta neredeyse doğrusaldır. Bükülmenin şiddetli olduğu bölgede "
           "naif ortalama daha çok sapar." % (Z[0] / Z[2])),
      h2("Örnek piksel hesabı", "4.4"),
      para("Koyu bölgeden alınan bir komşu piksel çifti için işlem adım adım gösterilmiştir."),
      mono("Dosyadaki (kodlu, sRGB) degerler\n"
           "  E0 = %.4f  (8 bit %d)        E1 = %.4f  (8 bit %d)\n\n"
           "Adim 1 - coz\n"
           "  L0 = %.4f^2.2 = %.5f\n"
           "  L1 = %.4f^2.2 = %.5f\n\n"
           "Adim 2 - dogrusal uzayda ortala\n"
           "  Lort = (%.5f + %.5f) / 2 = %.5f\n\n"
           "Adim 3 - yeniden kodla\n"
           "  E = %.5f^(1/2.2) = %.4f  ->  8 bit %d      DOGRU\n\n"
           "Naif yol\n"
           "  (%.4f + %.4f) / 2 = %.4f  ->  8 bit %d      YANLIS\n\n"
           "Fark: %.4f  ->  %.2f ton; naif sonuc daha koyu."
           % (e0, round(e0 * 255), e1, round(e1 * 255),
              e0, dec(e0), e1, dec(e1),
              dec(e0), dec(e1), (dec(e0) + dec(e1)) / 2,
              (dec(e0) + dec(e1)) / 2, CORR_P, round(CORR_P * 255),
              e0, e1, NAIF_P, round(NAIF_P * 255),
              CORR_P - NAIF_P, (CORR_P - NAIF_P) * 255)),
      fig("07_gamma_ortalama.png",
          "Şekil 7. Yarı boyuta indirme sonucu: üstte naif yöntem, ortada doğru yöntem, altta ton "
          "cinsinden hata. Hata soldaki koyu bölgede yoğunlaşmaktadır.", 140 * mm),
      fig("08_hata_egrisi.png",
          "Şekil 8. Hatanın taban parlaklığına göre değişimi. Eğri tekdüze azalmakta, koyu uçta "
          "yaklaşık altı kat yüksek değer almaktadır.", 112 * mm),
      h2("Değerlendirme", "4.5")]
S += items([
    "Uç durumda sekiz bit ölçekte 58 ton sapma ölçülmüştür.",
    "Hata her zaman aynı işaretlidir; naif sonuç daima olması gerekenden koyudur. Kodlama "
    "fonksiyonu konkav olduğundan fark tek yönlüdür. Bu nedenle hata rastgele gürültü değil "
    "sistematik yanlılıktır ve üst üste uygulanan işlemlerde birikir.",
    "Hata koyu bölgede açık bölgeye göre yaklaşık 3.6 kat büyüktür.",
    "Doğrusallaştırma, değer birleştiren tüm işlemler için gereklidir: yeniden boyutlandırma, alfa "
    "harmanlama, piramit inşası, çok kareli HDR ve gürültü giderme ortalamaları. Yalnızca "
    "sıralamaya dayanan işlemler için gerekmez, çünkü gamma monoton artan bir dönüşümdür ve "
    "büyüklük sırasını korur."])
S += [PageBreak()]

# ------------------------------------------------------------------ 5. L1.4
S += [h1("Yer Örnekleme Aralığı ve Şerit Genişliği", 5),
      h2("Problem tanımı", "5.1"),
      para("İğne deliği modelinde bir nesnenin görüntüdeki boyutu benzer üçgenlerden elde edilir. "
           "Odak uzaklığı katalogda milimetre cinsinden belirtildiğinden, piksel cinsinden "
           "karşılığı için önce piksel boyutu hesaplanmalıdır. Yer örnekleme aralığı, bir pikselin "
           "yeryüzünde karşılık geldiği mesafedir ve izdüşüm bağıntısında görüntü boyutu bir piksel "
           "alınarak elde edilir."),
      mono("s_px = W_s / N_x = 13.2 / 5472        = 2.412281e-03 mm/px\n"
           "f_x  = f / s_px  = 8.8 / 2.4123e-03   = 3648.0 piksel\n"
           "       birim kontrolu:  mm / (mm/px) = px\n\n"
           "GSD   = Z / f_x\n"
           "Serit = GSD x N_x = Z x W_s / f"),
      para("Hesaplarda Çözümlü Örnek 1.1 ile aynı kamera kullanılmıştır: sensör genişliği 13.2 mm, "
           "yatay çözünürlük 5472 piksel, fiziksel odak uzaklığı 8.8 mm."),
      h2("Bulgular", "5.2"),
      tbl([["Z (m)", "GSD (m/px)", "GSD (cm/px)", "Şerit (m)", "120 m'ye göre"],
           ["60", "%.6f" % GSD[60], "%.2f" % (GSD[60] * 100), "%.1f" % (GSD[60] * N_X), "0.50 kat"],
           ["120", "%.6f" % GSD[120], "%.2f" % (GSD[120] * 100), "%.1f" % (GSD[120] * N_X),
            "referans"],
           ["240", "%.6f" % GSD[240], "%.2f" % (GSD[240] * 100), "%.1f" % (GSD[240] * N_X),
            "2.00 kat"]],
          [20 * mm, 28 * mm, 28 * mm, 26 * mm, 32 * mm],
          "Çizelge 7. Uçuş yüksekliğine göre yer örnekleme aralığı ve taranan şerit genişliği."),
      para("120 m satırı Çözümlü Örnek 1.1 sonucuyla birebir örtüşmektedir (3.29 cm/px). Bu, hesap "
           "zincirinin doğru kurulduğunu göstermektedir."),
      h2("Çapraz doğrulama", "5.3"),
      para("Şerit genişliği ikinci ve bağımsız bir yoldan, yatay görüş açısı üzerinden de "
           "hesaplanmıştır. Yatay görüş açısı 2 arctan(W<sub>s</sub> / 2f) = %.2f derece bulunmuş, "
           "şerit genişliği 2 Z tan(FOV/2) bağıntısıyla üç yükseklik için yeniden elde edilmiştir. "
           "Üç durumda da iki yol arasındaki fark tam olarak sıfırdır; hesapta birim veya cebir "
           "hatası bulunmamaktadır." % FOV),
      fig("09_gsd.png",
          "Şekil 9. Yer örnekleme aralığı ve şerit genişliğinin uçuş yüksekliğiyle değişimi. İki "
          "büyüklük de doğrusaldır; işaretli noktalar hesaplanan üç yüksekliği göstermektedir."),
      h2("Değerlendirme", "5.4")]
S += items([
    "GSD = Z / f<sub>x</sub> bağıntısında f<sub>x</sub> kameranın sabitidir; tek serbest değişken "
    "uçuş yüksekliğidir. Bu nedenle yer örnekleme aralığı yükseklikle doğrusal ölçeklenir ve "
    "ölçülen oranlar tam 2.0000 çıkmıştır.",
    "Geometrik nedeni, görüş konisinin sabit açıyla açılmasıdır. Yükseklik iki katına çıktığında "
    "koni yeryüzünde iki kat geniş bir alanı tarar; piksel sayısı değişmediğinden her piksele düşen "
    "yer alanı da iki katına çıkar.",
    "Şerit genişliği bu kamera için 1.5 Z kapalı formuna indirgenmektedir.",
    "Tasarım ödünleşimi: yükseklik arttıkça tek geçişte taranan alan genişler, buna karşılık her "
    "pikselin yer çözünürlüğü kabalaşır. 10 cm hedef çözünürlük için gereken yükseklik "
    "0.10 &times; 3648 &#8776; 365 m olup Çözümlü Örnek 1.1'in (d) şıkkıyla tutarlıdır."])
S += [PageBreak()]

# ------------------------------------------------------------------ 6. sonuç
S += [h1("Genel Değerlendirme", 6),
      para("Dört görev, dijital kamera işlem hattının farklı adımlarındaki bilgi kaybını aynı "
           "yöntemle ele almıştır: kayıp denetimli biçimde üretilmiş, geri kazanım denenmiş ve "
           "kalan fark uygun bir metrikle ölçülmüştür. Her görevde elde edilen değer, ders "
           "kapsamında verilen kuramsal ifadeyle karşılaştırılmış ve tutarlı bulunmuştur."),
      tbl([["Görev", "Ölçülen büyüklük", "Sonuç", "Doğrulanan ifade"],
           ["L1.1", "PSNR", "G %.2f / R %.2f / B %.2f dB" % (PS[1], PS[0], PS[2]),
            "Renk verisinin üçte ikisi kestirimdir"],
           ["L1.2", "SNR eğimi", "%.3f dB/bit" % SLOPE, "Her bit SNR'ı 6.02 dB artırır"],
           ["L1.3", "Ton hatası", "58 ton (uç durum)", "Kodlu uzayda ortalama yanlıştır"],
           ["L1.4", "GSD", "1.64 / 3.29 / 6.58 cm/px", "GSD, yükseklikle doğrusaldır"]],
          [16 * mm, 30 * mm, 46 * mm, 58 * mm],
          "Çizelge 8. Görevlerin özeti ve doğrulanan kuramsal ifadeler."),
      para("Ortak çıkarım, her adımda kaybedilen bilginin geri getirilemeyeceği ve sonraki tüm "
           "işlemlerin bu kayıpların üzerine kurulduğudur. Bölüm 2'de silinen renk örnekleri, "
           "Bölüm 3'te yuvarlanan genlik farkları ve Bölüm 4'te kodlama sırasında değiştirilen "
           "değer ölçeği, sonradan uygulanan hiçbir işlemle tam olarak geri kazanılamaz. Bu nedenle "
           "algoritma tasarımında hangi halkanın hata ürettiğini bilmek, hatayı sonradan gidermeye "
           "çalışmaktan daha belirleyicidir."),
      para("Yöntemsel bir not olarak, Bölüm 3.4'te kuramsal ifadenin sabit teriminin "
           "gözlenmemesi, bir formülün ezberlenmesi ile türetiminin bilinmesi arasındaki farkı "
           "ortaya koymaktadır. Aynı biçimde Bölüm 5.3'teki çapraz doğrulama, bir sonucun yalnızca "
           "üretilmesinin değil, bağımsız bir yoldan sınanmasının da gerekli olduğunu "
           "göstermektedir."),
      h2("Ekler", "6.1"),
      para("Çalıştırılabilir kod, 23 kod hücresinden oluşan BIL458_Odev1.ipynb adlı Jupyter "
           "defteridir ve Google Colab ortamında değişiklik gerektirmeden çalışır. Görev başına "
           "bağımsız betikler L1_1.py, L1_2.py, L1_3.py ve L1_4.py dosyalarıdır. Raporda yer alan "
           "dokuz şekil out dizininde saklanmaktadır. Test görüntüsü, defterin ilk hücresi "
           "tarafından otomatik olarak indirilmektedir."),
      h2("Kaynaklar", "6.2"),
      Paragraph("Szeliski, R. (2022). <i>Computer Vision: Algorithms and Applications</i> "
                "(2. baskı). Springer. Bölüm 2.3.1, 2.3.2 ve 10.3.1.", LI, bulletText="[1]"),
      Paragraph("Bayer, B. E. (1976). <i>Color imaging array</i>. ABD Patenti No. 3.971.065.",
                LI, bulletText="[2]"),
      Paragraph("Gezer, M. (2026). <i>BİL458 Bilgisayarlı Görme, Hafta 1 ders notları</i>. "
                "İstanbul Medeniyet Üniversitesi.", LI, bulletText="[3]"),
      Paragraph("Eastman Kodak Company. <i>Kodak PhotoCD test görüntü kümesi</i>, kodim19.",
                LI, bulletText="[4]")]


# ------------------------------------------------------------------ belge
class Doc(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        toc_ref = getattr(flowable, "_toc", None)
        if toc_ref:
            self.notify("TOCEntry", (toc_ref[0], toc_ref[1], self.page))


def deco(canvas, doc_):
    canvas.saveState()
    if doc_.page > 1:
        canvas.setFont("HeadR", 8)
        canvas.setFillColor(GREY)
        canvas.drawString(24 * mm, 13 * mm, "BİL458 Bilgisayarlı Görme · Ödev 1")
        canvas.drawRightString(A4[0] - 24 * mm, 13 * mm, "%d" % doc_.page)
        canvas.setStrokeColor(colors.HexColor("#cccccc"))
        canvas.setLineWidth(0.4)
        canvas.line(24 * mm, 16.5 * mm, A4[0] - 24 * mm, 16.5 * mm)
    canvas.restoreState()


doc = Doc(str(WEEK1 / "BIL458_Odev1_Rapor.pdf"), pagesize=A4,
          leftMargin=24 * mm, rightMargin=24 * mm,
          topMargin=22 * mm, bottomMargin=22 * mm,
          title="BIL458 Odev 1 - Kamera Islem Hattinda Bilgi Kaybinin Olculmesi",
          author="Sevban Bozaslan")
doc.multiBuild(S, onFirstPage=deco, onLaterPages=deco)
print("PDF yazildi:", (WEEK1 / "BIL458_Odev1_Rapor.pdf").name)
