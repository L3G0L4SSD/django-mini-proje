from django.urls import include, path    
from . import views
from .views import tum_yazilar,ana_sayfa,test_view,register,profil_guncelle

urlpatterns = [
    
    path('',views.ana_sayfa , name='ana_sayfa'),
    path('guncelle/<int:id>/', views.guncelle,name='guncelle'),
    path('sil/<int:id>/',views.sil ,name='sil'), 
    path('yazilar/',views.tum_yazilar,name='tum_yazilar'),
    path('yazi/<int:id>/',views.yazi_detay,name='yazi_detay'),
    path('test/',test_view,name='test_view'),
    path('register/',register,name='register'),
    path('profil_guncelle/',profil_guncelle,name='profil_guncelle'),
    path("hesap_sil/",views.hesap_sil,name="hesap_sil"),
    path("giris/",views.kullanici_giris,name="giris"),
    
]