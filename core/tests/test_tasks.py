from django.test import TestCase 
from unittest.mock import patch, MagicMock 
from core.tasks import pasif_ilanlari_kontrol_et, haftalik_aktivite_raporu, aylik_aktivite_raporu 
from core.models import IsIlanlari, Aktivite 
from django.utils import timezone 
 
class TaskTests(TestCase): 
 
    @patch('core.tasks.IsIlanlari.objects.filter') 
    def test_pasif_ilanlari_kontrol_et(self, mock_filter): 
        mock_update = MagicMock() 
        mock_filter.return_value.update = mock_update 
        mock_update.return_value = 3 
 
        result = pasif_ilanlari_kontrol_et() 
 
        mock_filter.assert_called_once() 
        mock_update.assert_called_once_with(statu='pasif') 
        self.assertEqual(result, "3 adet ilan pasif yapıldı") 
 
    @patch('core.tasks.Aktivite.objects.filter') 
    @patch('core.tasks.canvas.Canvas') 
    @patch('core.tasks.os.makedirs') 
    def test_haftalik_aktivite_raporu(self, mock_makedirs, mock_canvas, mock_filter): 
        mock_filter.return_value = [] 
        mock_canvas_instance = MagicMock() 
        mock_canvas.return_value = mock_canvas_instance 
 
        result = haftalik_aktivite_raporu() 
 
        mock_makedirs.assert_called_once_with('reports', exist_ok=True) 
        mock_canvas.assert_called_once() 
        self.assertIn('haftalik_aktivite_raporu', result) 
 
    @patch('core.tasks.Aktivite.objects.filter') 
    @patch('core.tasks.canvas.Canvas') 
    @patch('core.tasks.os.makedirs') 
    def test_aylik_aktivite_raporu(self, mock_makedirs, mock_canvas, mock_filter): 
        mock_filter.return_value = [] 
        mock_canvas_instance = MagicMock() 
        mock_canvas.return_value = mock_canvas_instance 
 
        result = aylik_aktivite_raporu() 
 
        mock_makedirs.assert_called_once_with('reports', exist_ok=True) 
        mock_canvas.assert_called_once() 
        self.assertIn('aylik_aktivite_raporu', result) 
