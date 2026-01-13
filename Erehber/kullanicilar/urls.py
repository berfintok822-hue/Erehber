from django.urls import path
from . import views

urlpatterns = [
    path('kayit-ol/', views.kayit_ol, name='kayit_ol'),
    path('giris-yap/', views.giris_yap, name='login'),
    path('cikis-yap/', views.cikis_yap, name='logout'),
    path('profil/', views.profil, name='profil'),
]
