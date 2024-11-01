# WebP Dönüştürücü

WebP Dönüştürücü, JPG ve PNG formatındaki görüntüleri WebP formatına dönüştüren kullanımı kolay bir masaüstü uygulamasıdır.

## Özellikler

- Tek dosya veya toplu klasör dönüştürme
- Kalite ayarı (1-100 arası)
- Orijinal dosyaları silme seçeneği
- Klasör yapısını koruma seçeneği
- Özel dosya isimlendirme
- Dönüştürme sonuçlarını detaylı görüntüleme
- Kolay kullanımlı grafiksel arayüz

## Kurulum

1. Python 3.6 veya üzeri sürümünün yüklü olduğundan emin olun
2. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```

## Kullanım

Programı başlatmak için:
```bash
python webp-converter.py
```

1. "Dosya Seç" veya "Klasör Seç" butonlarıyla dönüştürmek istediğiniz görüntüleri seçin
2. İsteğe bağlı olarak hedef klasörü seçin
3. Kalite ayarını yapın (varsayılan: 80%)
4. İsterseniz diğer seçenekleri ayarlayın:
   - Orijinal dosyaları sil
   - Klasör yapısını koru
   - Dosya adlarını değiştir
5. "Dönüştür" butonuna tıklayın

## Gereksinimler

- Python 3.6+
- Pillow
- tkinter (Python ile birlikte gelir)

