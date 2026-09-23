# BİL458 Bilgisayarlı Görme

Sevban Bozaslan, 23120205020. İstanbul Medeniyet Üniversitesi, Bilgisayar Mühendisliği.
Dersi veren: Doç. Dr. Murat Gezer. 2026-2027 Güz.

Her hafta `weekN/` dizininde: hoca slaytı (`HaftaN.pdf`), o haftanın ödev kodu ve iki PDF.
Ana kaynak kitap: `Szeliski_CVAABook_2ndEd.pdf` (üst dizinde, git'e dahil değil).
Kitapta **PDF sayfası = kitap sayfası + 26**.

## Çalışma akışı

Sevban konuyu bilmeden başlıyor. Sıra şu, atlanırsa işe yaramıyor:

1. **Slaytı oku**, ödevin ne istediğini çıkar. Slaytlar kendi içinde tutarsız olabiliyor
   (Hafta 1'de teslim tarihi üç yerde üç farklı yazıyordu). Classroom'daki başlık bağlayıcı.
2. **Kavramları sıfırdan anlat.** Formül değil mekanizma. Sevban "hiçbir şey bilmiyorum"
   dediğinde gerçekten bilmiyor, temelden başla. Kitap referans kitabı, ders kitabı değil;
   sıfırdan öğretmiyor, çevirtmek vakit kaybı.
3. Sevban "anladım" diyene kadar **kod yazma.** Onay cümlesi gelmeden tek satır yazma.
4. Kodu **adım adım** yaz, her adımı çalıştırıp sonucu göster.
5. Sonunda iki PDF: teslim raporu + Sevban'ın kendisi için kavram notu.

## Teslim biçimi

- Classroom'a **rapor PDF + çalıştırılabilir kod**. Kod Colab'a yükleniyor, link veriliyor.
- Notebook tek `.ipynb`, ilk hücre test görüntüsünü internetten indiriyor (Colab'da dosya
  yükleme derdi olmasın diye).
- Ayrıca görev başına bağımsız `.py` betikleri.

## Sevban'ın tercihleri

- **Em dash kesinlikle yasak.** En dash de kullanma. Kısa tire veya orta nokta. PDF üretiminde
  `—` ve `&mdash;` kaçış dizilerini de kontrol et, gözden kaçıyor.
- **Rapor dili:** resmi akademik, üçüncü şahıs, edilgen çatı.
- **Kavram notu dili:** konuşma dili, sen-dili, kısa cümleler. "AI gibi" yazma:
  "Bedeli şudur", "Kritik nokta şudur", "Sonuç olarak" gibi kalıplar ve her paragrafta
  aynı ritim onu rahatsız ediyor.
- **Kısa tut.** Kavram notu 4-5 sayfa. 19 sayfa yazınca "ders kitabı olmuş" dedi.
- **Tasarım:** klasik akademik. Renk yok, gölge yok, yuvarlak köşe yok, kart yok.
  Web sayfası havası istemiyor.
- Sormadan iş büyütme, sormadan dosya oluşturma. Onay cümlesi: "tamam", "yap", "devam", "ok".

## PDF üretimi

`tools/rapor_sablonu.py` ve `tools/kavram_sablonu.py` çalışan şablonlar. Hafta 1 içeriğiyle
dolular; yeni hafta için içeriği değiştir, yapıyı koru.

- **reportlab** kullanılıyor (nbconvert, pandoc, weasyprint yok).
- **Font:** gövde Cambria (`cambria.ttc`, `subfontIndex=0`), başlık Calibri Bold, kod Consolas.
  Constantia kullanma: old-style rakam basıyor, tablolarda sayılar sarkık çıkıyor.
- **LaTeX:** tam kurulum yok. matplotlib mathtext ile formülü 420 dpi şeffaf PNG basıp
  gömüyoruz, Computer Modern fontuyla gerçek LaTeX gibi duruyor. `bmatrix` desteklenmiyor,
  matrisler mono kutuda kalıyor. `\le` yerine `\leq` yaz.
- Rapor yapısı: kapak, içindekiler (`multiBuild` ile), numaralı bölümler, çizelge ve şekil
  numaralandırması, üst bilgi ve sayfa numarası, kaynakça.

## Bu ortamda takılınan yerler

- **`cv2.imread` Türkçe karakterli yolu okuyamıyor.** Görüntü okurken PIL kullan.
- **Bash heredoc apostrof gören yerde patlıyor** (`unexpected EOF`). Uzun Python yaması
  yazacaksan Write ile dosyaya yaz, sonra çalıştır.
- Konsola Türkçe basarken `PYTHONIOENCODING=utf-8` gerekiyor.
- matplotlib'i başsız çalıştırmak için `MPLBACKEND=Agg`.
- Python 3.12, numpy 1.26, opencv 4.11, skimage 0.24, reportlab var. nbformat yok
  (notebook JSON'u elle üretiliyor).

## Git

Sevban commit'i kendi atıyor. Asla commit veya push yapma, sadece okuma komutları.

## Hafta 1 (bitti)

Ödev 1, laboratuvar görevleri L1.1-L1.4: Bayer demozaikleme (PSNR), nicemleme gürültüsü
(SNR eğimi), gamma uzayında ortalama hatası, GSD hesabı. Test görüntüsü Kodak kodim19
(Lenna kullanılmadı, IEEE 2024'ten beri kabul etmiyor).

Çıkan sonuçlar: PSNR G 31.22 / R 26.29 / B 26.58 dB, SNR eğimi 6.021 dB/bit,
gamma sapması 58 ton, GSD 1.64 / 3.29 / 6.58 cm/px.

Raporda vurgulanan iki ince nokta: yeşilin dört komşudan, kırmızı ve mavinin iki komşudan
kestirilmesi (PSNR farkının sebebi), ve slayttaki 1.76 dB sabitinin sinüs girişe ait olması
(rampada sabit sıfır çıkıyor, ölçüm bunu doğruladı).
