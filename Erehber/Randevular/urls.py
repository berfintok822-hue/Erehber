from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("randevu-al/", views.randevu_al, name="randevu_al"),
    path("randevu-listesi/", views.randevu_listesi, name="randevu_listesi"),
    path("psikologlar/", views.psikologlar, name="psikologlar"),
    path("psikolog-panel/", views.psikolog_panel, name="psikolog_panel"),
    path("randevu/<int:pk>/durum/", views.randevu_durum_guncelle, name="randevu_durum_guncelle"),
]