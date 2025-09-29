# �K Y�netim Sistemi 
 
Bu proje, �nsan Kaynaklar� y�netimi i�in kapsaml� bir Django uygulamas�d�r. 
 
## �zellikler 
 
- ? Django + PostgreSQL + Docker 
- ? Session ve JWT Authentication 
- ? Object-Based Yetkilendirme 
- ? �� �lanlar� Y�netimi 
- ? Aday Profilleri ve CV Y�netimi 
- ? Aday Ak��lar� ve Aktivite Takibi 
- ? Celery Task'lar� 
- ? Loglama Sistemi 
- ? Kapsaml� Testler 
- ? Performans Optimizasyonu 
- ? Raporlama (PDF/LaTeX) 
 
## Kurulum 
 
\`\`\`bash 
docker-compose up -d 
docker-compose exec web python manage.py migrate 
docker-compose exec web python manage.py createsuperuser 
\`\`\` 
