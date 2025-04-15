from django.contrib import admin
from django.contrib.auth.admin import   UserAdmin
from django.contrib.auth.models import User
# Register your models here.
from .models import Yazi

class Yaziadmin(admin.ModelAdmin):
    list_display= ('baslik','yazar','goruntulenme_sayisi','olusturulma_tarihi')
    list_filter =('olusturulma_tarihi','yazar')#filtreleme
    search_fields=('baslik','icerik')#arama alanları 
    ordering =('-olusturulma_tarihi',)#varsayılan sıralama

admin.site.register(Yazi,Yaziadmin)