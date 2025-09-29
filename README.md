# òK Yînetim Sistemi 
 
Bu proje, ònsan Kaynaklarç yînetimi iáin kapsamlç bir Django uygulamasçdçr. 
 
## ôzellikler 
 
- ? Django + PostgreSQL + Docker 
- ? Session ve JWT Authentication 
- ? Object-Based Yetkilendirme 
- ? òü òlanlarç Yînetimi 
- ? Aday Profilleri ve CV Yînetimi 
- ? Aday Akçülarç ve Aktivite Takibi 
- ? Celery Task'larç 
- ? Loglama Sistemi 
- ? Kapsamlç Testler 
- ? Performans Optimizasyonu 
- ? Raporlama (PDF/LaTeX) 
 
## Kurulum 
 
\`\`\`bash 
docker-compose up -d 
docker-compose exec web python manage.py migrate 
docker-compose exec web python manage.py createsuperuser 
\`\`\` 
