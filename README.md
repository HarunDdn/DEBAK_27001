# DEBAK BGYS — ISO 27001 Bilgi Güvenliği Yönetim Sistemi

DEBAK kuruluşuna ait ISO/IEC 27001:2013 standardına uygun Bilgi Güvenliği Yönetim Sistemi (BGYS) web uygulamasıdır.

## Özellikler

- **Varlık Yönetimi** — Bilgi varlıklarının envanteri ve sınıflandırılması
- **Risk Değerlendirme** — Risk kayıtları, olasılık/etki matrisi ve muamele planları
- **Politika Yönetimi** — Bilgi güvenliği politikalarının oluşturulması ve takibi
- **Olay Yönetimi** — Güvenlik olaylarının kaydı, izlenmesi ve çözülmesi
- **Kontrol Takibi** — ISO 27001 Annex A (114 kontrol) uyum durumu izleme
- **Gösterge Paneli** — Genel uyum durumu ve açık risk/olay özeti

## Kurulum

### Gereksinimler

- Python 3.9+

### Adımlar

```bash
# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Uygulamayı başlatın (veritabanı otomatik oluşturulur)
python run.py
```

Tarayıcıda `http://localhost:5000` adresini açın.

### Ortam Değişkenleri (İsteğe Bağlı)

| Değişken | Açıklama | Varsayılan |
|---|---|---|
| `SECRET_KEY` | Flask oturum anahtarı | Rastgele güvenli anahtar (her başlatmada yenilenir) |
| `DATABASE_URL` | SQLAlchemy veritabanı bağlantı dizesi | `sqlite:///instance/bgys.db` |

## Proje Yapısı

```
├── app/
│   ├── __init__.py        # Uygulama fabrikası ve Annex A tohumlaması
│   ├── models.py          # Veritabanı modelleri
│   ├── routes/            # Blueprint route'ları
│   │   ├── main.py        # Gösterge paneli
│   │   ├── assets.py      # Varlık yönetimi
│   │   ├── risks.py       # Risk değerlendirme
│   │   ├── policies.py    # Politika yönetimi
│   │   ├── incidents.py   # Olay yönetimi
│   │   └── controls.py    # ISO 27001 kontrol takibi
│   └── templates/         # Jinja2 HTML şablonları
├── config.py              # Uygulama konfigürasyonu
├── run.py                 # Uygulama giriş noktası
├── requirements.txt       # Python bağımlılıkları
└── tests/
    └── test_app.py        # Birim testleri
```

## Testler

```bash
pip install pytest
pytest tests/
```

## Lisans

© DEBAK — Tüm hakları saklıdır.
