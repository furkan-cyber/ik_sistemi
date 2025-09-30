# İK Yönetim Sistemi - Kapsamlı Kurulum ve Kullanım Kılavuzu

## 📋 İçindekiler

1. [Proje Hakkında](#proje-hakkında)
2. [Özellikler](#özellikler)
3. [Teknoloji Stack](#teknoloji-stack)
4. [Sistem Gereksinimleri](#sistem-gereksinimleri)
5. [Docker ile Kurulum](#docker-ile-kurulum)
6. [Projeyi Başlatma](#projeyi-başlatma)
7. [API Dokümantasyonu](#api-dokümantasyonu)
8. [Kullanım Senaryoları](#kullanım-senaryoları)
9. [Test İşlemleri](#test-işlemleri)
10. [Sorun Giderme](#sorun-giderme)
11. [Proje Yapısı](#proje-yapısı)
12. [Katkıda Bulunma](#katkıda-bulunma)

---

## 🎯 Proje Hakkında

**İK Yönetim Sistemi**, insan kaynakları firmalarının aday yönetimi, iş ilanı takibi ve CV analizi süreçlerini dijitalleştiren kapsamlı bir web uygulamasıdır. Sistem, Django REST Framework tabanlı modern bir backend, PostgreSQL veritabanı ve Redis destekli Celery görev kuyruğu ile güçlendirilmiştir.

### Ana Kullanım Alanları

- İK firmaları için müşteri firma yönetimi
- İş ilanı oluşturma ve takip
- Toplu CV yükleme ve otomatik parsing (NLTK destekli)
- Aday akış süreçlerini yönetme
- Aktivite ve durum takibi
- Otomatik raporlama ve bildirimler

---

## ✨ Özellikler

### 🏢 Firma Yönetimi
- **İK Firma Tanımları**: Çoklu İK firması desteği
- **Müşteri Firma Yönetimi**: Sektör bazlı müşteri firma takibi
- **Yetkilendirme Sistemi**: Kullanıcı bazlı firma erişim kontrolü

### 📝 İş İlanı Yönetimi
- İş ilanı oluşturma, düzenleme ve silme
- Aktif/Pasif durum yönetimi
- Kapanış tarihi otomasyonu (Celery ile)
- Müşteri firmaya göre filtreleme

### 👤 Aday Yönetimi
- Detaylı aday profilleri
- Eğitim bilgileri takibi
- İş deneyimi kayıtları
- **Toplu CV Yükleme**: PDF ve DOCX formatında
- **AI Destekli CV Parsing**: NLTK kütüphanesi ile otomatik bilgi çıkarma
  - İsim, soyisim, email, telefon
  - Eğitim bilgileri
  - İş deneyimleri
  - Yetenek ve beceriler

### 📊 Aday Akış Yönetimi
- İlan bazlı aday takibi
- Aktivite kayıtları (Telefon, Email, Test)
- Durum (Statu) yönetimi
- Zaman damgalı aktivite geçmişi

### 🔄 Otomatik İşlemler (Celery)
- Günlük pasif ilan kontrolü
- Haftalık aktivite raporları
- Aylık aktivite raporları
- PDF rapor oluşturma

### 🔐 Güvenlik
- JWT tabanlı authentication
- Rol bazlı yetkilendirme
- Firma bazlı veri izolasyonu
- CSRF ve XSS koruması

---

## 🛠 Teknoloji Stack

### Backend
- **Django 4.2.7**: Web framework
- **Django REST Framework 3.14.0**: API geliştirme
- **PostgreSQL 13**: Veritabanı
- **Redis 6**: Cache ve message broker
- **Celery 5.3.4**: Asenkron görev yönetimi
- **Celery Beat**: Periyodik görev zamanlayıcı

### AI/ML & Parsing
- **NLTK 3.8.1**: Doğal dil işleme
- **PDFPlumber 0.10.3**: PDF metin çıkarma
- **python-docx 1.1.0**: Word dosyası işleme
- **ReportLab 4.0.4**: PDF rapor oluşturma

### DevOps
- **Docker & Docker Compose**: Konteynerizasyon
- **Gunicorn**: Production WSGI server
- **WhiteNoise**: Static dosya servisi

---

## 💻 Sistem Gereksinimleri

### Minimum Gereksinimler
- **İşletim Sistemi**: Linux, macOS, Windows (WSL2 önerilir)
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **RAM**: En az 4GB (8GB önerilir)
- **Disk**: 10GB boş alan

### Önerilen Gereksinimler
- **İşletim Sistemi**: Ubuntu 22.04 LTS veya macOS
- **Docker**: En son sürüm
- **RAM**: 8GB+
- **Disk**: 20GB+ SSD
- **CPU**: 4 core+

---

## 🚀 Docker ile Kurulum

### 1. Projeyi Klonlama

```bash
# GitHub'dan projeyi klonlayın
git clone https://github.com/furkan-cyber/ik_sistemi.git

# Proje dizinine gidin
cd ik_sistemi
```

### 2. Ortam Değişkenlerini Yapılandırma

`.env` dosyası zaten projede mevcut. Üretim ortamı için bu değerleri güncelleyin:

```bash
# .env dosyasını düzenleyin
nano .env
```

**Önemli Değişkenler:**

```env
# ÜRETİM ORTAMI İÇİN DEĞİŞTİRİN!
SECRET_KEY=django-insecure-your-unique-secret-key-here-change-this
DEBUG=False  # Üretimde False olmalı

# Veritabanı (güçlü şifre kullanın)
DB_PASSWORD=cok_guclu_bir_sifre_123!@#

# İzin verilen hostlar (domain'inizi ekleyin)
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# CSRF güvenliği (domain'inizi ekleyin)
CSRF_TRUSTED_ORIGINS=http://localhost:8000,https://yourdomain.com
```

### 3. Docker Container'larını Başlatma

```bash
# Container'ları oluştur ve başlat
docker-compose up -d

# Logları izle (opsiyonel)
docker-compose logs -f
```

**Container'lar:**
- `web`: Django uygulaması (Port: 8000)
- `db`: PostgreSQL veritabanı (Port: 5432)
- `redis`: Redis cache (Port: 6379)

### 4. Veritabanı Migrasyonları

```bash
# Migration'ları çalıştır
docker-compose exec web python manage.py migrate

# Superuser oluştur
docker-compose exec web python manage.py createsuperuser
```

Superuser bilgilerinizi girin:
```
Username: admin
Email: admin@example.com
Password: ********
```

### 5. Static Dosyaları Toplama

```bash
# Static dosyaları topla
docker-compose exec web python manage.py collectstatic --noinput
```

### 6. NLTK Verilerini İndirme

```bash
# NLTK verilerini indir (Dockerfile'da otomatik yapılır)
# Manuel indirmek isterseniz:
docker-compose exec web python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('maxent_ne_chunker'); nltk.download('stopwords')"
```

---

## 🎮 Projeyi Başlatma

### Hızlı Başlangıç

```bash
# Tüm servisleri başlat
docker-compose up -d

# Servislerin durumunu kontrol et
docker-compose ps

# Logları görüntüle
docker-compose logs -f web
```

### Uygulamaya Erişim

- **Ana Sayfa**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API Dokümantasyonu**: http://localhost:8000/api/
- **API Token**: http://localhost:8000/api/token/

### İlk Kullanım Adımları

1. **Admin panele giriş yapın**: http://localhost:8000/admin
   - Username: admin
   - Password: (oluşturduğunuz şifre)

2. **İK Firma oluşturun**:
   - Admin panel → IK Firmalar → Add
   - Firma adı ve açıklama girin

3. **Müşteri Firma ekleyin**:
   - Admin panel → Musteri Firmalar → Add
   - Firma adı ve sektör bilgisi girin

4. **İK User oluşturun**:
   - Admin panel → IK Users → Add
   - Kullanıcıyı İK firmaya bağlayın
   - Yetkili müşteri firmalar ekleyin

5. **İş ilanı oluşturun**:
   - Admin panel → Is Ilanlari → Add
   - Başlık, açıklama ve kapanış tarihi girin

---

## 📡 API Dokümantasyonu

### Authentication

**JWT Token Alma:**

```bash
# Token al
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "your_password"
  }'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Token Refresh:**

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }'
```

### İş İlanları API

**Tüm İlanları Listeleme:**

```bash
curl -X GET http://localhost:8000/api/is-ilanlari/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Yeni İlan Oluşturma:**

```bash
curl -X POST http://localhost:8000/api/is-ilanlari/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "ik_firma": 1,
    "musteri_firma": 1,
    "baslik": "Backend Developer",
    "aciklama": "Django ve Python uzmanı aranıyor",
    "kapanis_tarihi": "2025-12-31T23:59:59Z",
    "statu": "aktif"
  }'
```

**İlan Filtreleme:**

```bash
# Müşteri firmaya göre filtrele
curl -X GET "http://localhost:8000/api/is-ilanlari/?musteri_firma=1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Statüye göre filtrele
curl -X GET "http://localhost:8000/api/is-ilanlari/?statu=aktif" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Aday Yönetimi API

**Aday Listeleme:**

```bash
curl -X GET http://localhost:8000/api/adaylar/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Yeni Aday Ekleme:**

```bash
curl -X POST http://localhost:8000/api/adaylar/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "ad": "Ahmet",
    "soyad": "Yılmaz",
    "email": "ahmet.yilmaz@example.com",
    "telefon": "05551234567"
  }'
```

**Toplu CV Yükleme (Bulk Upload):**

```bash
curl -X POST http://localhost:8000/api/adaylar/bulk_upload/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "cv_files=@/path/to/cv1.pdf" \
  -F "cv_files=@/path/to/cv2.pdf" \
  -F "cv_files=@/path/to/cv3.docx"
```

**Response:**
```json
{
  "message": "3 dosya işlendi",
  "olusturulan_adaylar": [
    {
      "id": 1,
      "ad": "Mehmet",
      "soyad": "Demir",
      "email": "mehmet.demir@example.com",
      "durum": "oluşturuldu"
    },
    {
      "id": 2,
      "ad": "Ayşe",
      "soyad": "Kaya",
      "email": "ayse.kaya@example.com",
      "durum": "zaten mevcut"
    }
  ],
  "toplam": 2
}
```

### Aday Akış API

**Aday Akış Oluşturma:**

```bash
curl -X POST http://localhost:8000/api/aday-akis/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "is_ilani": 1,
    "aday": 1
  }'
```

**Aktivite Ekleme:**

```bash
curl -X POST http://localhost:8000/api/aday-akis/1/aktivite_ekle/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "aktivite_tipi": "telefon",
    "statu": 1,
    "aciklama": "Aday ile telefon görüşmesi yapıldı. Olumlu geri dönüş alındı."
  }'
```

---

## 💼 Kullanım Senaryoları

### Senaryo 1: Toplu CV İşleme

```python
import requests

# Token al
token_response = requests.post('http://localhost:8000/api/token/', json={
    'username': 'admin',
    'password': 'your_password'
})
token = token_response.json()['access']

# Toplu CV yükle
files = [
    ('cv_files', open('cv1.pdf', 'rb')),
    ('cv_files', open('cv2.pdf', 'rb')),
    ('cv_files', open('cv3.docx', 'rb'))
]

response = requests.post(
    'http://localhost:8000/api/adaylar/bulk_upload/',
    headers={'Authorization': f'Bearer {token}'},
    files=files
)

print(response.json())
```

### Senaryo 2: İlan Oluşturma ve Aday Eşleştirme

```python
import requests
from datetime import datetime, timedelta

token = "YOUR_ACCESS_TOKEN"
headers = {'Authorization': f'Bearer {token}'}

# 1. İş ilanı oluştur
ilan_data = {
    'ik_firma': 1,
    'musteri_firma': 1,
    'baslik': 'Python Developer',
    'aciklama': 'Django ve Flask deneyimi olan developer aranıyor',
    'kapanis_tarihi': (datetime.now() + timedelta(days=30)).isoformat(),
    'statu': 'aktif'
}

ilan_response = requests.post(
    'http://localhost:8000/api/is-ilanlari/',
    headers=headers,
    json=ilan_data
)
ilan_id = ilan_response.json()['id']

# 2. Adayları listele
adaylar = requests.get(
    'http://localhost:8000/api/adaylar/',
    headers=headers
).json()

# 3. Uygun adayları ilana ekle
for aday in adaylar['results']:
    akis_data = {
        'is_ilani': ilan_id,
        'aday': aday['id']
    }
    requests.post(
        'http://localhost:8000/api/aday-akis/',
        headers=headers,
        json=akis_data
    )
```

### Senaryo 3: Aktivite Takibi

```python
# Aday akışına aktivite ekle
aktivite_data = {
    'aktivite_tipi': 'telefon',
    'statu': 1,  # "Olumlu" statüsünün ID'si
    'aciklama': 'Aday ile ilk telefon görüşmesi yapıldı. Teknik beceriler uygun.'
}

response = requests.post(
    f'http://localhost:8000/api/aday-akis/{akis_id}/aktivite_ekle/',
    headers=headers,
    json=aktivite_data
)
```

---

## 🧪 Test İşlemleri

### Unit Testleri Çalıştırma

```bash
# Tüm testleri çalıştır
docker-compose exec web python manage.py test

# Belirli bir uygulamanın testlerini çalıştır
docker-compose exec web python manage.py test core

# Belirli bir test dosyasını çalıştır
docker-compose exec web python manage.py test core.tests.test_models

# Coverage ile çalıştır
docker-compose exec web coverage run --source='.' manage.py test
docker-compose exec web coverage report
docker-compose exec web coverage html
```

### Test Yapısı

```
ik_sistemi/core/tests/
├── __init__.py
├── test_models.py      # Model testleri
├── test_views.py       # API endpoint testleri
└── test_tasks.py       # Celery görev testleri
```

### Örnek Test Çıktısı

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
......................
----------------------------------------------------------------------
Ran 22 tests in 3.456s

OK
```

---

## 🔧 Sorun Giderme

### Container Sorunları

**Problem**: Container başlamıyor
```bash
# Container loglarını kontrol et
docker-compose logs web

# Container'ı yeniden başlat
docker-compose restart web

# Tüm container'ları yeniden oluştur
docker-compose down
docker-compose up -d --build
```

**Problem**: Port çakışması
```bash
# Kullanılan portları kontrol et
sudo lsof -i :8000
sudo lsof -i :5432

# docker-compose.yml'de portları değiştir
ports:
  - "8001:8000"  # 8000 yerine 8001
```

### Veritabanı Sorunları

**Problem**: Veritabanı bağlantı hatası
```bash
# PostgreSQL container'ını kontrol et
docker-compose exec db psql -U ik_user -d ik_sistemi

# Veritabanını sıfırla
docker-compose down -v
docker-compose up -d
docker-compose exec web python manage.py migrate
```

**Problem**: Migration hataları
```bash
# Migration dosyalarını temizle
docker-compose exec web find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
docker-compose exec web find . -path "*/migrations/*.pyc"  -delete

# Yeniden migrate et
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### NLTK Sorunları

**Problem**: NLTK verileri bulunamıyor
```bash
# NLTK verilerini manuel indir
docker-compose exec web python -c "
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('stopwords')
nltk.download('words')
"
```

### CV Parsing Sorunları

**Problem**: PDF okuma hatası
```bash
# PDFPlumber bağımlılıklarını kontrol et
docker-compose exec web pip install --upgrade pdfplumber

# Test dosyası ile dene
docker-compose exec web python manage.py shell
>>> from core.utils import cv_parser
>>> result = cv_parser.extract_text_from_file('/app/test.pdf')
>>> print(result)
```

### Redis Sorunları

**Problem**: Redis bağlanamıyor
```bash
# Redis container'ını kontrol et
docker-compose exec redis redis-cli ping
# Beklenen çıktı: PONG

# Redis loglarını kontrol et
docker-compose logs redis
```

### Permission Sorunları

**Problem**: Dosya yazma izni yok
```bash
# Media ve reports dizinlerine izin ver
docker-compose exec web mkdir -p media reports
docker-compose exec web chmod -R 777 media reports
```

---

## 📁 Proje Yapısı

```
ik_sistemi/
├── core/                          # Ana uygulama
│   ├── migrations/                # Veritabanı migration'ları
│   ├── static/                    # Static dosyalar
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   ├── templates/                 # HTML şablonları
│   │   └── index.html
│   ├── tests/                     # Test dosyaları
│   │   ├── test_models.py
│   │   ├── test_views.py
│   │   └── test_tasks.py
│   ├── admin.py                   # Admin panel yapılandırması
│   ├── models.py                  # Veritabanı modelleri
│   ├── serializers.py             # DRF serializer'ları
│   ├── views.py                   # API view'ları
│   ├── urls.py                    # URL yapılandırması
│   ├── permissions.py             # İzin sınıfları
│   ├── tasks.py                   # Celery görevleri
│   └── utils.py                   # Yardımcı fonksiyonlar (CV Parser)
├── ik_sistemi/                    # Proje ayarları
│   ├── __init__.py
│   ├── settings.py                # Django ayarları
│   ├── urls.py                    # Ana URL yapılandırması
│   ├── wsgi.py                    # WSGI yapılandırması
│   └── celery.py                  # Celery yapılandırması
├── media/                         # Yüklenen dosyalar
├── reports/                       # Oluşturulan raporlar
├── staticfiles/                   # Toplanan static dosyalar
├── .env                           # Ortam değişkenleri
├── .gitignore
├── docker-compose.yml             # Docker Compose yapılandırması
├── Dockerfile                     # Docker image tanımı
├── manage.py                      # Django yönetim script'i
├── requirements.txt               # Python bağımlılıkları
└── README.md                      # Bu dosya
```

---

## 🔄 Celery Görevleri

### Periyodik Görevler

Celery Beat ile zamanlanmış görevler (şu anda docker-compose.yml'de kapalı):

```python
# core/tasks.py içeriği

@shared_task
def pasif_ilanlari_kontrol_et():
    """Kapanış tarihi geçmiş ilanları pasif yapar"""
    simdi = timezone.now()
    pasif_yapilan = IsIlanlari.objects.filter(
        kapanis_tarihi__lt=simdi,
        statu='aktif'
    ).update(statu='pasif')
    return f"{pasif_yapilan} adet ilan pasif yapıldı"

@shared_task
def haftalik_aktivite_raporu():
    """Haftalık aktivite raporu PDF oluşturur"""
    # PDF oluşturma kodu
    return dosya_adi

@shared_task
def aylik_aktivite_raporu():
    """Aylık aktivite raporu PDF oluşturur"""
    # PDF oluşturma kodu
    return dosya_adi
```

### Celery'yi Aktifleştirme

Celery servislerini kullanmak için `docker-compose.yml` dosyasındaki ilgili bölümlerin yorumunu kaldırın:

```yaml
celery:
  build: .
  command: celery -A ik_sistemi worker -l info
  # ... diğer ayarlar

celery-beat:
  build: .
  command: celery -A ik_sistemi beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
  # ... diğer ayarlar
```

Ardından:

```bash
docker-compose up -d celery celery-beat
```

---

## 🌐 Production Deployment

### Güvenlik Kontrol Listesi

- [ ] `DEBUG=False` olarak ayarla
- [ ] Güçlü `SECRET_KEY` oluştur
- [ ] `ALLOWED_HOSTS` ve `CSRF_TRUSTED_ORIGINS` güncelle
- [ ] Veritabanı şifrelerini değiştir
- [ ] HTTPS yapılandır
- [ ] Firewall kurallarını ayarla
- [ ] Backup stratejisi oluştur
- [ ] Log izleme sistemi kur

### Nginx Reverse Proxy (Opsiyonel)

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/ik_sistemi/staticfiles/;
    }

    location /media/ {
        alias /path/to/ik_sistemi/media/;
    }
}
```

---

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen şu adımları izleyin:

1. Bu repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'feat: Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

### Commit Mesajı Formatı

```
feat: Yeni özellik
fix: Hata düzeltme
docs: Dokümantasyon güncellemesi
style: Kod formatı
refactor: Kod düzenleme
test: Test ekleme/güncelleme
chore: Rutin görevler
```

---

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

---

## 👨‍💻 İletişim

- **GitHub**: [@furkan-cyber](https://github.com/furkan-cyber)
- **Repository**: [ik_sistemi](https://github.com/furkan-cyber/ik_sistemi)

---

## 🆘 Destek

Sorun yaşıyorsanız:

1. [Issues](https://github.com/furkan-cyber/ik_sistemi/issues) bölümünü kontrol edin
2. Yeni bir issue oluşturun (detaylı açıklama ve log ekleyin)
3. Dokümantasyonu tekrar okuyun

---

**Not**: Bu proje aktif geliştirme aşamasındadır. Önerileriniz ve katkılarınız değerlidir!


