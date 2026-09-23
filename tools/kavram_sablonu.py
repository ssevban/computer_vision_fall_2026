# -*- coding: utf-8 -*-
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (KeepTogether, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

WEEK1 = Path("C:/Users/sevba/Masa\u00fcst\u00fc/\u00fcni/im\u00fc/computer_vision_2026_fall/week1")
F = "C:/Windows/Fonts/"
pdfmetrics.registerFont(TTFont("Body", F + "cambria.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("BodyB", F + "cambriab.ttf"))
pdfmetrics.registerFont(TTFont("BodyI", F + "cambriai.ttf"))
pdfmetrics.registerFont(TTFont("Head", F + "calibrib.ttf"))
pdfmetrics.registerFont(TTFont("HeadR", F + "calibri.ttf"))
pdfmetrics.registerFont(TTFont("Mono", F + "consola.ttf"))
pdfmetrics.registerFontFamily("Body", normal="Body", bold="BodyB", italic="BodyI")

INK = colors.HexColor("#111111")
GREY = colors.HexColor("#4f4f4f")
LIGHT = colors.HexColor("#8a8a8a")
HAIR = colors.HexColor("#c4c4c4")
BOX = colors.HexColor("#f2f2f0")
KEY = colors.HexColor("#7d3a1d")

BODY = ParagraphStyle("BODY", fontName="Body", fontSize=9.9, leading=14,
                      alignment=TA_JUSTIFY, textColor=INK, spaceAfter=5)
TITLE = ParagraphStyle("TITLE", fontName="Head", fontSize=16, leading=20,
                       textColor=INK, spaceAfter=2)
SUB = ParagraphStyle("SUB", fontName="BodyI", fontSize=10, leading=14,
                     textColor=GREY, spaceAfter=12)
H = ParagraphStyle("H", fontName="Head", fontSize=11.5, leading=15, textColor=INK,
                   spaceBefore=11, spaceAfter=5)
MONO = ParagraphStyle("MONO", fontName="Mono", fontSize=8.3, leading=11.8,
                      textColor=INK)
LI = ParagraphStyle("LI", parent=BODY, leftIndent=13, bulletIndent=2, spaceAfter=3)
KEYP = ParagraphStyle("KEYP", fontName="Body", fontSize=9.9, leading=13.6,
                      textColor=INK, alignment=TA_JUSTIFY)


def p(t):
    return Paragraph(t, BODY)


def h(t):
    return Paragraph(t, H)


def li(lst):
    return [Paragraph(t, LI, bulletText="\u2022") for t in lst]


def box(text):
    t = Table([[Paragraph(text.replace(" ", "&nbsp;").replace("\n", "<br/>"), MONO)]],
              colWidths=[160 * mm], hAlign="CENTER")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BOX),
        ("BOX", (0, 0), (-1, -1), 0.3, HAIR),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return KeepTogether([Spacer(1, 2 * mm), t, Spacer(1, 3.5 * mm)])


def key(text):
    t = Table([[Paragraph(text, KEYP)]], colWidths=[160 * mm], hAlign="CENTER")
    t.setStyle(TableStyle([
        ("LINEBEFORE", (0, 0), (0, -1), 2.2, KEY),
        ("LEFTPADDING", (0, 0), (-1, -1), 11),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return KeepTogether([Spacer(1, 2.5 * mm), t, Spacer(1, 4 * mm)])


TBL = TableStyle([
    ("FONTNAME", (0, 0), (-1, 0), "Head"),
    ("FONTNAME", (0, 1), (-1, -1), "Body"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("TEXTCOLOR", (0, 0), (-1, -1), INK),
    ("LINEABOVE", (0, 0), (-1, 0), 0.9, INK),
    ("LINEBELOW", (0, 0), (-1, 0), 0.9, INK),
    ("LINEBELOW", (0, -1), (-1, -1), 0.9, INK),
    ("INNERGRID", (0, 1), (-1, -1), 0.25, HAIR),
    ("ALIGN", (0, 0), (0, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 3.2),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
])


def tbl(data, widths):
    t = Table(data, colWidths=widths, hAlign="CENTER")
    t.setStyle(TBL)
    return KeepTogether([Spacer(1, 2 * mm), t, Spacer(1, 4 * mm)])


import hashlib
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["mathtext.fontset"] = "cm"
import matplotlib.pyplot as plt
from reportlab.platypus import Image as RLImage

EQDIR = Path(__file__).parent / "_eq"
EQDIR.mkdir(exist_ok=True)


def eq(latex, size=13.5):
    name = hashlib.md5((latex + str(size)).encode("utf-8")).hexdigest()[:12] + ".png"
    fp = EQDIR / name
    if not fp.exists():
        fig = plt.figure(figsize=(0.01, 0.01))
        fig.text(0, 0, latex, fontsize=size)
        fig.savefig(str(fp), dpi=420, transparent=True, bbox_inches="tight", pad_inches=0.04)
        plt.close(fig)
    from PIL import Image as PILImage
    w, h = PILImage.open(fp).size
    scale = 72.0 / 420.0
    img = RLImage(str(fp), width=w * scale, height=h * scale)
    img.hAlign = "CENTER"
    return KeepTogether([Spacer(1, 2.5 * mm), img, Spacer(1, 3.5 * mm)])


S = []

S += [Paragraph("Hafta 1 Kavram Notları", TITLE),
      Paragraph("BİL458. Ödev 1'deki dört görevin arkasında ne var.", SUB)]

# ---------------------------------------------------------------- 1
S += [h("1. Renk sensörü: bir piksel neyi ölçemiyor"),
      p("Sensördeki her hücre bir fotodiyot. Üstüne foton düşüyor, elektrona çeviriyor, pozlama "
        "bitince tek bir sayı veriyor: buraya şu kadar ışık geldi."),
      p("Ama bu hücre renk körü. Gelen fotonun dalga boyunu ayırt edemiyor, sadece sayıyor. Kırmızı "
        "foton da mavi foton da onun için aynı şey."),
      p("O zaman renk nereden geliyor? Her hücrenin üstüne renkli bir cam koyuyorsun. Kırmızı cam "
        "sadece kırmızıyı geçiriyor, gerisini yutuyor. Hücre yine tek sayı veriyor ama o sayı artık "
        "buradaki kırmızı miktarı demek. Bedeli de şu: o hücre kırmızı ölçüyorsa yeşili ve maviyi "
        "hiç ölçmüyor. Kayıp burada başlıyor."),
      p("Peki camları nasıl dizeceksin? Bayer 1976'da şunu önerdi, 2x2 blok, tüm sensöre döşeniyor:"),
      box("R G R G          hucrelerin %25'i R\n"
          "G B G B                     %25'i B\n"
          "R G R G                     %50'si G\n"
          "G B G B"),
      p("<b>Neden iki tane yeşil var?</b> Cevap sensörde değil, senin gözünde. Parlaklığın çoğunu "
        "yeşil banttan alıyorsun. Bir de ince detayı parlaklıktan seçiyorsun, renkten değil. Bir "
        "teli parlaklık farkıyla net görürsün; aynı tel sadece renk farkıyla çizilseydi bulanık "
        "gelirdi. Detay demek parlaklık, parlaklık demek yeşil. O yüzden yeşile iki kat yer "
        "veriliyor, kırmızıyla mavi seyrek kalıyor ve sen farkı yakalayamıyorsun. Aynı numara "
        "JPEG'de de var: parlaklık tam kalıyor, renk yarıya iniyor, kimse anlamıyor."),
      key("Her pikselde bir gerçek ölçüm var, iki boşluk var. Boşlukları komşulardan tahmin etme "
          "işine <b>demozaikleme</b> deniyor. Yani renkli fotoğrafın verisinin üçte ikisi ölçüm "
          "değil, tahmin. L1.1'de ölçtüğün şey bu tahminin ne kadar tutmadığı.")]

# ---------------------------------------------------------------- 2
S += [h("2. PSNR: hata ne kadar, tek sayıyla"),
      p("İki görüntü ne kadar farklı? Önce en basit yol: her piksel için farkı al, karesini al, "
        "hepsini ortala. Buna MSE deniyor. Kareyi neden alıyorsun? Bir, işaretten kurtuluyorsun, "
        "+5 ile -5 aynı kötülükte. İki, büyük hatalar daha ağır cezalandırılıyor."),
      p("MSE'nin sorunu şu: sayıya bakıp bir şey anlamıyorsun. MSE 12 çıktı, iyi mi kötü mü? "
        "Görüntünün aralığını bilmeden söyleyemezsin. 0-255 aralığında 12 gayet iyi, 0-1 aralığında "
        "rezalet. PSNR bunu düzeltiyor: hatayı maksimum değere oranlıyor, sonra log alıyor."),
      eq(r"$\mathrm{MSE}=\mathrm{ort}\left[(I-\hat{I})^{2}\right]"
         r"\qquad\qquad \mathrm{PSNR}=10\,\log_{10}\dfrac{\mathrm{MAX}^{2}}{\mathrm{MSE}}$"),
      p("MAX 8 bitte 255. Örnek: ortalama 3 birimlik hata yapıyorsan MSE 9 olur, PSNR da 38.6 dB "
        "çıkar."),
      p("Log almanın sebebi: hata oranları çok geniş aralıkta geziyor, log bunu sıkıştırıp okunur "
        "hale getiriyor. Bir de dB sinyal işlemenin ortak dili, L1.2'deki 6 dB/bit ile doğrudan "
        "karşılaştırabiliyorsun. Çıkan sayıyı şöyle okuyacaksın:"),
      tbl([["PSNR", "Ne demek"],
           ["40 dB üstü", "farkı gözle göremezsin"],
           ["30 - 40 dB", "iyi, dikkatli bakarsan kenarlarda seçilir"],
           ["20 - 30 dB", "bozulma belli oluyor"],
           ["20 dB altı", "görüntü bariz bozuk"]],
          [30 * mm, 118 * mm]),
      p("Senin ödevde çıkan değerler: yeşil 31.22, kırmızı 26.29, mavi 26.58 dB.")]

# ---------------------------------------------------------------- 3
S += [h("3. Bilineer interpolasyon: boşluğu nasıl dolduruyorsun"),
      p("İstediğin çıktıda her pikselde üç sayı olacak. Elindeki veride her pikselde bir sayı var. "
        "Yani her piksel için iki sayı eksik. Burada kafa karışıyor: kırmızı konumunda kırmızı "
        "ölçülü olması o pikseli kurtarmıyor, onun da yeşili ve mavisi yok, onları da doldurman "
        "gerek. Nasıl dolduruyorsun? O kanalın bilindiği komşuların ortalamasını alıyorsun."),
      box("(2,2) konumu, filtresi R, okudugu 125\n"
          "  R : olculu, 125\n"
          "  G : dort dik komsu     (160+165+135+155)/4 = 153.75\n"
          "  B : dort kosegen komsu (60+70+55+75)/4     = 65\n\n"
          "(2,1) konumu, filtresi G, okudugu 145\n"
          "  G : olculu, 145\n"
          "  R : sadece YATAYDA kirmizi komsu var -> (105+115)/2 = 110\n"
          "  B : sadece DIKEYDE mavi komsu var    -> (60+55)/2   = 57.5"),
      p("Dikkat et: piksellerin yarısı yeşil ve iki yeşil tipi birbirinin tersi. Birinde kırmızı "
        "yataydan geliyor, diğerinde dikeyden. Yani dört konum tipin var, üç değil."),
      key("Yeşili <b>hep dört komşudan</b> buluyorsun. Kırmızıyla maviyi bazen <b>iki komşudan, tek "
          "yönden</b>. PSNR farkı tam olarak buradan çıkıyor."),
      p("Kodda bu dört durumu tek tek yazmıyorsun, iki konvolüsyon çekirdeği hepsini hallediyor. "
        "Numara şu: çekirdeği ham veriye değil, maskelenmiş seyrek diziye uyguluyorsun. Ölçüm "
        "olmayan yerler sıfır, sıfırlar toplama katkı yapmıyor, yani çekirdek kendiliğinden sadece "
        "doğru komşuları topluyor. Ağırlıklar da her konumda toplamı 4 verecek şekilde seçilmiş, o "
        "yüzden tek bölme her durumda doğru ortalamayı veriyor."),
      box("K_G  =  0 1 0          K_RB =  1 2 1\n"
          "        1 4 1                  2 4 2\n"
          "        0 1 0  / 4             1 2 1  / 4")]

# ---------------------------------------------------------------- 4
S += [h("4. Zipper: tek yönden tahmin etmenin bedeli"),
      p("Tek satır düşün, ortasında siyahtan beyaza keskin bir geçiş var. Gerçekte hepsi gri, yani "
        "üç kanal eşit. Sensör sadece kendi filtresinin kanalını okuyor, sonra sen eksikleri "
        "dolduruyorsun:"),
      box("piksel:    p0    p1    p2    p3    p4    p5\n"
          "gercek:     0     0     0    255   255   255\n"
          "filtre:     R     G     R     G     R     G\n\n"
          "p2'nin G'si eksik -> komsu G'ler p1=0 ve p3=255 -> G = 127.5\n"
          "p2'nin R'si olculu ve 0   ->  p2 = (R=0, G=127.5)\n"
          "                              yesile kacti, oysa tam siyah olmaliydi\n\n"
          "p3'un R'si eksik -> komsu R'ler p2=0 ve p4=255 -> R = 127.5\n"
          "p3'un G'si olculu ve 255  ->  p3 = (R=127.5, G=255)\n"
          "                              bu da yesile kacti, oysa tam beyaz olmaliydi"),
      p("Gri bir kenarda sahnede hiç olmayan bir renk üredi. Sebep basit: her kanalı farklı "
        "komşulardan dolduruyorsun, kenar geçişi kanallara farklı anlarda yansıyor, üçü senkronu "
        "kaçırıyor. İki boyutta bu kayma kenar boyunca piksel piksel yön değiştiriyor, kenar dişli "
        "ve renk saçaklı çıkıyor. Adı buradan geliyor."),
      p("Frekans tarafından bakarsan: interpolasyon alçak geçiren filtre, kenar ise yüksek frekans. "
        "Kırmızıyla mavi iki piksel aralıkla örneklendiği için Nyquist sınırları yarıya inmiş, "
        "yüksek frekans düşük frekansa katlanıyor. Buna örtüşme deniyor. Yeşil daha sık "
        "örneklendiği için daha az etkileniyor. Düz bölgelerde hata yok, çünkü orada komşular zaten "
        "birbirine eşit. Senin ölçümünde kenar pikselleri düz piksellerin 6.4 katı hata yaptı.")]

# ---------------------------------------------------------------- 5
S += [h("5. Nicemleme ve SNR: her bit neden 6 dB"),
      p("Fotodiyot sürekli bir gerilim üretiyor ama bilgisayar sürekli değer saklayamaz, sonlu "
        "seviyeye yuvarlaman gerek. B bit kullanırsan 2<super>B</super> seviyen olur, iki seviye "
        "arası mesafeye Δ diyoruz. Gerçek değer araya düşerse en yakın seviyeye yuvarlanıyor, o fark "
        "bir daha geri gelmiyor."),
      eq(r"$\Delta=\dfrac{1}{2^{B}}\qquad\quad"
         r"-\dfrac{\Delta}{2}\;\leq\;e\;\leq\;+\dfrac{\Delta}{2}\qquad\quad"
         r"\sigma_{e}^{2}=\dfrac{\Delta^{2}}{12}$"),
      box("B=2 -> 4 seviye,   delta = 0.25   (elindekiler: 0, 0.25, 0.50, 0.75)\n"
          "B=8 -> 256 seviye, delta = 0.0039"),
      p("SNR de sinyal gücünün gürültü gücüne oranı, dB cinsinden. Peki 6.02 nereden çıkıyor? Şöyle "
        "takip et:"),
      ]
S += li([
    "B'yi bir artırıyorsun, seviye sayısı ikiye katlanıyor, Δ yarıya iniyor.",
    "Hata gücü Δ² ile orantılı, yani dörde bölünüyor.",
    "Sinyal aynı kaldı, gürültü dörde bölündü. SNR dört katına çıktı.",
    "Dört katı dB'ye çevir: 10 log<sub>10</sub>(4) = 6.02 dB.",
])
S += [key("Eklediğin her bit SNR'ı sabit 6.02 dB artırıyor. O yüzden grafikte düz bir doğru çıkması "
          "lazım, eğimi de 6.02 olmalı. L1.2'de ölçtüğün eğim 6.021 çıktı."),
      p("<b>1.76 tuzağı.</b> Slayttaki formül SNR = 6.02·B + 1.76 diyor. O sabit, girişin "
        "tam ölçekli sinüs olduğu varsayımından geliyor, değeri 10 log<sub>10</sub>(1.5). Senin "
        "nicemlediğin şey ise rampa. Değerleri aralığa düzgün dağıldığı için sabit sıfırlanıyor, SNR "
        "tam olarak 6.02·B çıkıyor. Eğim iki durumda da aynı, değişen sadece sabit. Ödev de zaten "
        "sadece eğimi soruyor."),
      p("<b>Bant oluşumu.</b> Düşük bitte rampada gözle görülür basamaklar çıkıyor. B eşittir 3'te "
        "sadece sekiz seviyen var, yumuşak geçiş olması gereken yerde sekiz düz şerit görüyorsun. "
        "Göz düz alanlar arasındaki küçük süreksizlikleri abartarak algıladığı için bu rahatsız "
        "edici oluyor.")]

# ---------------------------------------------------------------- 6
S += [h("6. Gamma: dosyadaki sayılar ışık değil"),
      p("Işık fiziksel olarak doğrusal toplanıyor, sensör de doğrusal ölçüyor. Ama göz logaritmik "
        "algılıyor. Bir mum yanarken bir mum daha yakarsan farkı bariz görürsün; yüz mum yanarken "
        "aynı bir mumu hiç fark etmezsin. Yani karanlıktaki küçük farklara duyarlısın, aydınlıktaki "
        "aynı farka neredeyse körsün."),
      p("Sekiz bitle doğrusal saklarsan ne oluyor? Aydınlık tarafta gözünün ayıramadığı seviyelere "
        "bit harcıyorsun, karanlık tarafta seviye yetmiyor. Çözüm, kaydetmeden önce değerleri "
        "eğriyle yeniden dağıtmak. Bilgisayarındaki her JPEG ve PNG böyle kodlanmış."),
      eq(r"$I_{\mathrm{kodlu}}=I_{\mathrm{dogrusal}}^{\,1/\gamma}"
         r"\qquad\qquad \gamma\approx2.2$"),
      box("SIYAH (0) ve BEYAZ (1) pikselini ortala:\n\n"
          "  YANLIS:  (0 + 1) / 2 = 0.5000                   8 bitte 128\n"
          "  DOGRU :  coz    -> 0^2.2 = 0,  1^2.2 = 1\n"
          "           ortala -> 0.5\n"
          "           kodla  -> 0.5^(1/2.2) = 0.7297         8 bitte 186\n\n"
          "  fark: 58 ton"),
      p("Ortalama almak doğrusal bir işlem, gamma kodlaması değil. Kodlu değerleri doğrudan "
        "ortalarsan hata yapıyorsun. Üstelik hata rastgele de değil: x<super>1/2.2</super> eğrisi "
        "konkav olduğu için <b>naif sonuç her zaman olması gerekenden koyu</b> çıkıyor."),
      key("Hata en çok koyu bölgede. Eğrinin türevi x sıfıra giderken sonsuza gidiyor, yani eğri "
          "koyu tarafta çok dik, açık tarafta neredeyse düz. L1.3'te ölçtüğün oran 3.6 katı: koyuda "
          "6.96 ton, açıkta 1.93 ton."),
      p("<b>Nerede birikiyor:</b> değer birleştiren her işlemde. Yeniden boyutlandırma, alfa "
        "harmanlama, Gauss piramidi (her seviyede tekrar tekrar), çok kareli HDR. "
        "<b>Nerede gerekmiyor:</b> sadece sıralamaya bakan işlemlerde. Eşikleme, histogram germe, "
        "min ve maks. Çünkü gamma monoton artan, büyüklük sırasını bozmuyor.")]

# ---------------------------------------------------------------- 7
S += [h("7. GSD: bir piksel yerde kaç santim"),
      p("İğne deliği modeli benzer üçgenlerden x = f·X/Z veriyor. Ama f katalogda "
        "milimetre cinsinden yazıyor, sen x'i piksel cinsinden istiyorsun. O yüzden önce f'i piksele "
        "çeviriyorsun, sonra bir pikselin yerde kaç metreye denk geldiğini buluyorsun."),
      eq(r"$s_{px}=\dfrac{W_{s}}{N_{x}}\qquad f_{x}=\dfrac{f}{s_{px}}"
         r"\qquad \mathrm{GSD}=\dfrac{Z}{f_{x}}"
         r"\qquad \mathrm{serit}=Z\,\dfrac{W_{s}}{f}$"),
      box("s_px = 13.2 / 5472       = 2.4123e-03 mm/px\n"
          "f_x  = 8.8 / 2.4123e-03  = 3648 piksel      birim: mm / (mm/px) = px\n\n"
          "   Z = 60 m  ->  GSD 1.64 cm/px  ->  serit  90 m\n"
          "   Z = 120 m ->  GSD 3.29 cm/px  ->  serit 180 m\n"
          "   Z = 240 m ->  GSD 6.58 cm/px  ->  serit 360 m\n\n"
          "bu kamera icin  serit = 1.5 * Z"),
      p("GSD = Z/f<sub>x</sub> bağıntısında f<sub>x</sub> kameranın sabiti, tek oynayan Z. Yükseklik "
        "iki katına çıkınca çözünürlük yarıya düşüyor. Geometrik sebebi de şu: görüş konisi sabit "
        "açıyla açılıyor, yükseldikçe yerde daha geniş bir alanı tarıyor ama piksel sayın "
        "değişmiyor, aynı pikselleri daha geniş alana bölüştürüyorsun."),
      key("Ödünleşim: yükselirsen tek geçişte geniş şerit tararsın ama her piksel kabalaşır. "
          "Alçalırsan detay artar ama aynı alanı kaplamak için çok daha fazla geçiş gerekir. "
          "Uzaktan algılama tasarımının tamamı bu iki ucun arasındaki seçim.")]

# ---------------------------------------------------------------- özet
S += [h("Özet"),
      tbl([["Kavram", "Tek cümlede"],
           ["Bayer RGGB", "Yeşil yarıyı kaplıyor, çünkü parlaklık detayı yeşilden geliyor."],
           ["Demozaikleme", "Renk verisinin üçte ikisi ölçüm değil tahmin."],
           ["PSNR", "10 log<sub>10</sub>(255² / MSE); yüksekse hata az."],
           ["Bilineer", "Yeşil hep 4 komşudan, kırmızı ve mavi bazen 2 komşu tek yön."],
           ["Zipper", "Kanalları ayrı doldurunca kenarda olmayan renk doğuyor."],
           ["Nicemleme", "Δ = 1/2<super>B</super>, hata varyansı Δ²/12."],
           ["6.02 dB/bit", "Bit arttıkça Δ yarıya, hata gücü dörde bölünüyor."],
           ["1.76 sabiti", "Sinüs girişe ait, rampada sabit sıfır."],
           ["Gamma", "I<super>1/2.2</super>; bitleri gözün duyarlı olduğu karanlığa ayırıyor."],
           ["Gamma hatası", "Kodlu uzayda ortalarsan sonuç hep koyu çıkıyor, en çok koyuda."],
           ["f<sub>x</sub>", "f bölü piksel boyutu, piksel cinsinden odak uzaklığı."],
           ["GSD", "Z/f<sub>x</sub>, bir pikselin yerdeki karşılığı, Z ile doğrusal."]],
          [32 * mm, 126 * mm]),
      p("<b>Dördünün ortak mantığı.</b> Hoca slaytta bir zincir çizdi: sahne, mercek, renk süzgeci, "
        "fotodiyot, ADC, demozaik, gama, JPEG. Her adım bilgi kaybediyor. Ödev de diyor ki bu "
        "zincirin dört adımını al, kaybı sayıyla ölç. Yani yeni bir şey öğrenmiyorsun, slaytta yazan "
        "iddiayı kanıtlıyorsun. Kaybedilen bilgi hiçbir işlemle geri gelmiyor; bir algoritma hata "
        "yaptığında hatayı sonradan düzeltmeye çalışmak yerine zincirin hangi halkasının onu "
        "ürettiğini bilmek işini görüyor.")]


def deco(canvas, doc_):
    canvas.saveState()
    canvas.setFont("HeadR", 7.5)
    canvas.setFillColor(LIGHT)
    canvas.drawRightString(A4[0] - 18 * mm, 11 * mm, "%d" % doc_.page)
    canvas.restoreState()


doc = SimpleDocTemplate(str(WEEK1 / "BIL458_Hafta1_Kavramlar.pdf"), pagesize=A4,
                        leftMargin=18 * mm, rightMargin=18 * mm,
                        topMargin=16 * mm, bottomMargin=16 * mm,
                        title="BIL458 Hafta 1 Kavram Notlari", author="Sevban Bozaslan")
doc.build(S, onFirstPage=deco, onLaterPages=deco)
print("PDF yazildi:", (WEEK1 / "BIL458_Hafta1_Kavramlar.pdf").name)
