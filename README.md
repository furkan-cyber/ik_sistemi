# İK Yönetim Sistemi (HR Management System)

Profesyonel insan kaynakları yönetimi için geliştirilmiş kapsamlı Django tabanlı web uygulaması.

## 📋 İçindekiler

- [Genel Bakış](#genel-bakış)
- [Özellikler](#özellikler)
- [Teknoloji Yığını](#teknoloji-yığını)
- [Kurulum](#kurulum)
- [Yapılandırma](#yapılandırma)
- [Kullanım](#kullanım)
- [API Dokümantasyonu](#api-dokümantasyonu)
- [Proje Yapısı](#proje-yapısı)
- [Testler](#testler)
- [Docker ile Çalıştırma](#docker-ile-çalıştırma)
- [Güvenlik](#güvenlik)
- [Katkıda Bulunma](#katkıda-bulunma)

## 🎯 Genel Bakış

İK Yönetim Sistemi, İK firmalarının müşteri firmalarına ait iş ilanlarını yönetmesini, aday havuzunu oluşturmasını ve aday süreçlerini takip etmesini sağlayan kapsamlı bir platformdur. Sistem, CV parsing, otomatik raporlama ve aktivite takibi gibi gelişmiş özellikler sunar.

### Temel İşlevler

- **İK Firma Yönetimi**: Birden fazla İK firmasını destekler
- **Müşteri Firma Yönetimi**: Her İK firması birden fazla müşteri firma ile çalışabilir
- **İş İlanları**: Müşteri firmalar için iş ilanı oluşturma ve yönetme
- **Aday Yönetimi**: CV yükleme, parsing ve profil oluşturma
- **Aday Akış Takibi**: Her aday için iş ilanı bazında süreç takibi
- **Aktivite Yönetimi**: Telefon araması, mail gönderimi, test gönderimi gibi aktivitelerin kaydı
- **Otomatik Raporlama**: Haftalık ve aylık aktivite raporları

## ✨ Özellikler

### 1. Çok Kiracılı Mimari (Multi-tenancy)
- Her İK firması kendi verilerine erişebilir
- Müşteri firma bazlı yetkilendirme
- Kullanıcı bazlı veri izolasyonu

### 2. Gelişmiş CV Parsing
- PDF ve DOCX formatlarını destekler
- NLTK tabanlı doğal dil işleme
- Otomatik bilgi çıkarma:
  - Kişisel bilgiler (ad, soyad, email, telefon)
  - Eğitim geçmişi
  - İş deneyimi
  - Yetenekler ve diller
- Toplu CV yükleme ve işleme

### 3. RESTful API
- JWT tabanlı kimlik doğrulama
- Swagger/OpenAPI dokümantasyonu
- Sayfalama ve filtreleme desteği
- Detaylı hata yönetimi

### 4. Arka Plan Görevleri (Celery)
- Otomatik ilan kapanış kontrolü
- Periyodik rapor oluşturma
- Asenkron CV işleme
- Scheduled task yönetimi

### 5. Raporlama
- PDF formatında raporlar
- Haftalık aktivite özeti
- Aylık aktivite özeti
- Özelleştirilebilir rapor şablonları

## 🛠 Teknoloji Yığını

### Backend
- **Django 4.2.7**: Web framework
- **Django REST Framework**: API geliştirme
- **PostgreSQL**: İlişkisel veritabanı
- **Redis**: Cache ve message broker
- **Celery**: Arka plan görevleri ve scheduled tasks
- **Celery Beat**: Periyodik görev zamanlayıcı

### Güvenlik ve Kimlik Doğrulama
- **JWT (SimpleJWT)**: Token tabanlı kimlik doğrulama
- **Django Permissions**: Rol bazlı erişim kontrolü

### Belge İşleme ve NLP
- **pdfplumber**: PDF okuma
- **python-docx**: DOCX okuma
- **NLTK**: Doğal dil işleme
- **ReportLab**: PDF rapor oluşturma

### DevOps
- **Docker & Docker Compose**: Konteynerizasyon
- **Nginx**: Reverse proxy
- **Gunicorn**: WSGI server
- **WhiteNoise**: Static dosya servisi

## 📦 Kurulum

### Gereksinimler

- Python 3.9+
- PostgreSQL 13+
- Redis 6+
- Docker & Docker Compose (opsiyonel)

### Yerel Kurulum

1. **Repoyu Klonlayın**
```bash
git clone <repository-url>
cd ik_sistemi
```

2. **Virtual Environment Oluşturun**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

3. **Bağımlılıkları Yükleyin**
```bash
pip install -r requirements.txt
```

4. **NLTK Verilerini İndirin**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('maxent_ne_chunker'); nltk.download('stopwords'); nltk.download('words')"
```

5. **PostgreSQL Veritabanı Oluşturun**
```sql
CREATE DATABASE ik_sistemi;
CREATE USER ik_user WITH PASSWORD 'ik_password';
ALTER ROLE ik_user SET client_encoding TO 'utf8';
ALTER ROLE ik_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ik_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ik_sistemi TO ik_user;
```

6. **Çevre Değişkenlerini Ayarlayın**
```bash
cp .env.example .env
# .env dosyasını düzenleyin
```

7. **Veritabanı Migrasyonlarını Çalıştırın**
```bash
python manage.py makemigrations
python manage.py migrate
```

8. **Superuser Oluşturun**
```bash
python manage.py createsuperuser
```

9. **Static Dosyaları Toplayın**
```bash
python manage.py collectstatic --noinput
```

10. **Sunucuyu Başlatın**
```bash
python manage.py runserver
```

## ⚙️ Yapılandırma

### Ortam Değişkenleri (.env)

```ini
# Django Ayarları
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Veritabanı
DB_NAME=ik_sistemi
DB_USER=ik_user
DB_PASSWORD=ik_password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Dosya Yükleme
MAX_UPLOAD_SIZE=10485760  # 10MB
ALLOWED_FILE_EXTENSIONS=pdf,docx,doc

# AI/ML
USE_AI_PARSER=True
AI_MODEL_NAME=bert-base-multilingual-cased

# Raporlama
REPORT_TIMEZONE=Europe/Istanbul
REPORT_LANGUAGE=tr

# Güvenlik
CSRF_TRUSTED_ORIGINS=http://localhost:8000
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Loglama
LOG_LEVEL=INFO
LOG_FILE=debug.log
```

### Celery Zamanlı Görevler

Celery Beat ile çalışan otomatik görevler:

1. **Pasif İlan Kontrolü**: Kapanış tarihi geçen ilanları pasif yapar
2. **Haftalık Aktivite Raporu**: Her hafta PDF rapor oluşturur
3. **Aylık Aktivite Raporu**: Her ay PDF rapor oluşturur

Zamanlı görevleri yapılandırmak için Django admin panelinden "Periodic Tasks" bölümünü kullanın.

## 🚀 Kullanım

### Web Arayüzü

Ana sayfa: `http://localhost:8000/`
Admin panel: `http://localhost:8000/admin/`

### API Endpoints

#### Kimlik Doğrulama

**Token Al**
```bash
POST /api/token/
Content-Type: application/json

{
    "username": "kullanici_adi",
    "password": "sifre"
}
```

**Token Yenile**
```bash
POST /api/token/refresh/
Content-Type: application/json

{
    "refresh": "refresh_token"
}
```

#### İş İlanları

**İlanları Listele**
```bash
GET /api/is-ilanlari/
Authorization: Bearer <access_token>
```

**İlan Oluştur**
```bash
POST /api/is-ilanlari/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "ik_firma": 1,
    "musteri_firma": 1,
    "baslik": "Backend Developer",
    "aciklama": "Python Django geliştirici aranıyor",
    "kapanis_tarihi": "2025-12-31T23:59:59Z",
    "statu": "aktif"
}
```

**İlan Detayı**
```bash
GET /api/is-ilanlari/{id}/
Authorization: Bearer <access_token>
```

**İlan Güncelle**
```bash
PUT /api/is-ilanlari/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "baslik": "Senior Backend Developer",
    "statu": "pasif"
}
```

#### Adaylar

**Adayları Listele**
```bash
GET /api/adaylar/
Authorization: Bearer <access_token>
```

**Aday Oluştur**
```bash
POST /api/adaylar/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "ad": "Ahmet",
    "soyad": "Yılmaz",
    "email": "ahmet@example.com",
    "telefon": "05551234567"
}
```

**Toplu CV Yükleme**
```bash
POST /api/adaylar/bulk_upload/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

cv_files: [file1.pdf, file2.docx, ...]
```

#### Aday Akışları

**Aday Akışlarını Listele**
```bash
GET /api/aday-akis/
Authorization: Bearer <access_token>
```

**Aday Akışı Oluştur**
```bash
POST /api/aday-akis/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "is_ilani": 1,
    "aday": 1
}
```

**Aktivite Ekle**
```bash
POST /api/aday-akis/{id}/aktivite_ekle/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "aktivite_tipi": "telefon",
    "statu": 1,
    "aciklama": "Aday ile görüşüldü"
}
```

### Filtreleme ve Sayfalama

**Filtreleme**
```bash
GET /api/is-ilanlari/?musteri_firma=1&statu=aktif
GET /api/adaylar/?ad=Ahmet&soyad=Yılmaz
```

**Sayfalama**
```bash
GET /api/adaylar/?page=2
GET /api/adaylar/?page_size=50
```

## 📂 Proje Yapısı

```
ik_sistemi/
├── core/                          # Ana uygulama
│   ├── migrations/                # Veritabanı migrasyonları
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
│   ├── __init__.py
│   ├── admin.py                   # Django admin yapılandırması
│   ├── models.py                  # Veri modelleri
│   ├── serializers.py             # DRF serializers
│   ├── views.py                   # API views
│   ├── permissions.py             # Özel izinler
│   ├── tasks.py                   # Celery görevleri
│   ├── utils.py                   # Yardımcı fonksiyonlar (CV Parser)
│   └── urls.py                    # URL yapılandırması
├── ik_sistemi/                    # Proje ayarları
│   ├── __init__.py
│   ├── settings.py                # Django ayarları
│   ├── urls.py                    # Ana URL yapılandırması
│   ├── celery.py                  # Celery yapılandırması
│   └── wsgi.py                    # WSGI yapılandırması
├── .env                           # Ortam değişkenleri
├── .gitignore
├── docker-compose.yml             # Docker Compose yapılandırması
├── Dockerfile                     # Docker image tanımı
├── manage.py                      # Django yönetim script'i
├── nginx.conf                     # Nginx yapılandırması
├── requirements.txt               # Python bağımlılıkları
└── README.md                      # Bu dosya
```

### Veri Modelleri

```
IKFirma (İK Firması)
├── IKUser (İK Kullanıcısı)
│   └── ManyToMany: MusteriFirma
│
MusteriFirma (Müşteri Firma)
│
IsIlanlari (İş İlanı)
├── ForeignKey: IKFirma
└── ForeignKey: MusteriFirma
│
Aday (Candidate)
├── Egitim (Education)
└── IsDeneyimi (Work Experience)
│
AdayAkis (Candidate Flow)
├── ForeignKey: Aday
├── ForeignKey: IsIlani
└── Aktivite (Activity)
    ├── ForeignKey: Statu
    ├── ForeignKey: IKUser
    └── ForeignKey: IKFirma
```

## 🧪 Testler

### Tüm Testleri Çalıştırma

```bash
python manage.py test
```

### Belirli Bir Testi Çalıştırma

```bash
python manage.py test core.tests.test_models
python manage.py test core.tests.test_views
python manage.py test core.tests.test_tasks
```

### Coverage Raporu

```bash
coverage run --source='.' manage.py test
coverage report
coverage html  # HTML rapor oluşturur
```

### Test Kapsamı

- **Model Testleri**: Tüm veri modellerinin oluşturulması ve ilişkileri
- **View Testleri**: API endpoint'lerinin işlevselliği ve yetkilendirme
- **Task Testleri**: Celery görevlerinin doğru çalışması

## 🐳 Docker ile Çalıştırma

### Servisleri Başlatma

```bash
docker-compose up -d
```

### Servisler

- **web**: Django uygulaması (Port 8000)
- **db**: PostgreSQL (Port 5432)
- **redis**: Redis (Port 6379)
- **celery**: Celery worker
- **celery-beat**: Celery beat scheduler
- **nginx**: Nginx reverse proxy (Port 80)

### Migrasyonları Çalıştırma

```bash
docker-compose exec web python manage.py migrate
```

### Superuser Oluşturma

```bash
docker-compose exec web python manage.py createsuperuser
```

### Logları İzleme

```bash
docker-compose logs -f
docker-compose logs -f web      # Sadece web servisi
docker-compose logs -f celery   # Sadece celery
```

### Servisleri Durdurma

```bash
docker-compose down
```

### Verileri Temizleme

```bash
docker-compose down -v  # Volume'ları da siler
```

## 🔒 Güvenlik

### Üretim Ortamı için Öneriler

1. **Secret Key**: Güçlü ve benzersiz bir SECRET_KEY kullanın
2. **DEBUG Modu**: Üretimde `DEBUG=False` olarak ayarlayın
3. **HTTPS**: SSL sertifikası kullanın
4. **Database**: Güçlü veritabanı şifreleri
5. **CORS**: Sadece güvenilir origin'lere izin verin
6. **Rate Limiting**: API rate limiting uygulayın
7. **Input Validation**: Tüm kullanıcı girdilerini doğrulayın
8. **Dependency Updates**: Düzenli güvenlik güncellemeleri

### Güvenlik Ayarları (Production)

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

## 📊 İzleme ve Loglama

### Log Dosyaları

- **debug.log**: Tüm uygulama logları
- **celery.log**: Celery görev logları

### Log Seviyeleri

- `DEBUG`: Detaylı geliştirme bilgileri
- `INFO`: Genel bilgi mesajları
- `WARNING`: Uyarı mesajları
- `ERROR`: Hata mesajları
- `CRITICAL`: Kritik hatalar

### Celery Monitoring

```bash
# Celery flower (web-based monitoring)
pip install flower
celery -A ik_sistemi flower
# http://localhost:5555
```

## 🤝 Katkıda Bulunma

1. Bu repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

### Kod Standartları

- PEP 8 Python stil kılavuzuna uyun
- Anlamlı commit mesajları yazın
- Test coverage'ı düşürmeyin
- Dokümantasyonu güncelleyin




## 🙏 Teşekkürler

Bu projeyi geliştirmede kullanılan açık kaynak kütüphanelere teşekkürler:
- Django ve Django REST Framework ekibi
- NLTK geliştiricileri
- Celery topluluğu
- PostgreSQL ve Redis ekipleri

---


