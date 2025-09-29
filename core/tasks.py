from celery import shared_task 
from django.utils import timezone 
from .models import IsIlanlari, Aktivite 
import logging 
from datetime import datetime 
from reportlab.pdfgen import canvas 
import os 
 
logger = logging.getLogger(__name__) 
 
@shared_task 
def pasif_ilanlari_kontrol_et(): 
   
    simdi = timezone.now() 
    pasif_yapilan = IsIlanlari.objects.filter( 
        kapanis_tarihi__lt=simdi, 
        statu='aktif' 
    ).update(statu='pasif') 
 
    logger.info(f"{pasif_yapilan} adet ilan pasif yapıldı") 
    return f"{pasif_yapilan} adet ilan pasif yapıldı" 
 
@shared_task 
def haftalik_aktivite_raporu(): 
    """Haftalık aktivite raporu oluşturur""" 
    yil_basi = datetime(datetime.now().year, 1, 1) 
    aktiviteler = Aktivite.objects.filter(created_at__gte=yil_basi) 

    # PDF rapor oluşturma
    dosya_adi = f'reports/haftalik_aktivite_raporu_{datetime.now().strftime("%Y%m%d")}.pdf'
    os.makedirs('reports', exist_ok=True)

    c = canvas.Canvas(dosya_adi)
    c.drawString(100, 800, "Haftalık Aktivite Raporu")
    c.drawString(100, 780, f"Tarih: {datetime.now().strftime('%d.%m.%Y')}")
    c.save()

    logger.info(f"Haftalık aktivite raporu oluşturuldu: {dosya_adi}")
    return dosya_adi

@shared_task
def aylik_aktivite_raporu():
    """Aylık aktivite raporu oluşturur"""
    yil_basi = datetime(datetime.now().year, 1, 1)
    aktiviteler = Aktivite.objects.filter(created_at__gte=yil_basi)

    # PDF rapor oluşturma
    dosya_adi = f'reports/aylik_aktivite_raporu_{datetime.now().strftime("%Y%m")}.pdf'
    os.makedirs('reports', exist_ok=True)

    c = canvas.Canvas(dosya_adi)
    c.drawString(100, 800, "Aylık Aktivite Raporu")
    c.drawString(100, 780, f"Tarih: {datetime.now().strftime('%m.%Y')}")
    c.save()

    logger.info(f"Aylık aktivite raporu oluşturuldu: {dosya_adi}")
    return dosya_adi
