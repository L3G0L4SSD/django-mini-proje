from django.db import models


# Create your models here.
class Yazi(models.Model):
    baslik =models.CharField(max_length=200)
    icerik =models.TextField()
    olusturulma_tarihi =models.DateTimeField(auto_now_add=True)
    yazar = models.CharField(max_length=100,default="Bilinmiyor")
    goruntulenme_sayisi = models.IntegerField(default=0)
    
    def __str__(self):
        return self.baslik
    
