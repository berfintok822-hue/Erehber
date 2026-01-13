from django.contrib import admin
from .models import Randevu, PsychologistProfile


@admin.register(Randevu)
class RandevuAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'psychologist', 'psychologist_user', 'date', 'time', 'status', 'created_at')
    list_filter = ('status', 'date', 'psychologist')
    search_fields = ('fullname', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Kişi Bilgileri', {
            'fields': ('user', 'fullname', 'email', 'phone')
        }),
        ('Randevu Detayları', {
            'fields': ('psychologist', 'psychologist_user', 'date', 'time', 'message')
        }),
        ('Durum', {
            'fields': ('status',)
        }),
        ('Zaman Bilgileri', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PsychologistProfile)
class PsychologistProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'active')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
