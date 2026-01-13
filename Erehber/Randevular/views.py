from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Randevu, PsychologistProfile
from django.db import models
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from django.conf import settings


@login_required(login_url='login')
def randevu_al(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        psychologist = request.POST.get('psychologist')
        # psychologist may be id (from DB) or plain text; try to resolve
        psychologist_user = None
        try:
            # if an id was posted
            pid = int(psychologist)
            psychologist_user = None
            from django.contrib.auth.models import User
            psychologist_user = User.objects.filter(id=pid).first()
            if psychologist_user:
                psychologist_name = psychologist_user.get_full_name() or psychologist_user.username
            else:
                psychologist_name = request.POST.get('psychologist_name', '')
        except Exception:
            psychologist_name = psychologist
        date = request.POST.get('date')
        time = request.POST.get('time')
        message = request.POST.get('message')
        
        randevu = Randevu.objects.create(
            user=request.user,
            fullname=fullname,
            email=email,
            phone=phone,
            psychologist=psychologist_name,
            psychologist_user=psychologist_user,
            date=date,
            time=time,
            message=message
        )
        # Göndericiye ve kullanıcıya e-posta bildirimi (geliştirme: console backend)
        try:
            subject = 'Randevu Başvurunuz Alındı'
            body = f"Merhaba {randevu.fullname},\n\nRandevunuz alınmıştır.\n\nPsikolog: {randevu.psychologist}\nTarih: {randevu.date}\nSaat: {randevu.time}\nDurum: {randevu.get_status_display()}\n\nTeşekkürler, Psyora"
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [randevu.email])
        except Exception:
            pass

        messages.success(request, 'Randevunuz başarıyla oluşturuldu! (E-posta bildirimi gönderildi)')
        return redirect('randevu_listesi')
    
    # Kullanıcının randevularını ve diğer tüm randevuları göster
    user_randevular = Randevu.objects.filter(user=request.user).order_by('-date', '-time')
    tum_randevular = Randevu.objects.filter(status='confirmed').order_by('date', 'time')
    # psikolog listesi
    psychologists = PsychologistProfile.objects.filter(active=True).select_related('user')
    
    context = {
        'title': 'Randevu Sayfası',
        'user_randevular': user_randevular,
        'tum_randevular': tum_randevular,
        'psychologists': psychologists,
    }
    
    return render(request, 'Randevu.html', context)


@login_required(login_url='login')
def randevu_listesi(request):
    randevular = Randevu.objects.filter(user=request.user).order_by('-date', '-time')
    context = {
        'title': 'Randevularım',
        'randevular': randevular,
    }
    return render(request, 'Randevu_Listesi.html', context)


@login_required(login_url='login')
def psikolog_panel(request):
    # Sadece psikolog hesabı olan kullanıcılar erişsin
    if not hasattr(request.user, 'psychologist_profile'):
        return HttpResponseForbidden('Bu sayfaya erişiminiz yok.')

    profile = request.user.psychologist_profile
    # Randevular: sadece kendisine atanmış randevular
    randevular = Randevu.objects.filter(psychologist_user=request.user).order_by('date', 'time')

    context = {
        'title': 'Psikolog Paneli',
        'profile': profile,
        'randevular': randevular,
    }
    return render(request, 'psikolog_panel.html', context)


@login_required(login_url='login')
def randevu_durum_guncelle(request, pk):
    # Psikologlar randevu durumunu güncelleyebilsin
    if not hasattr(request.user, 'psychologist_profile'):
        return HttpResponseForbidden('Bu işlem için yetkiniz yok.')

    randevu = get_object_or_404(Randevu, pk=pk)
    # Sadece kendisine atanmış randevuları değiştirsin
    if randevu.psychologist_user and randevu.psychologist_user != request.user:
        return HttpResponseForbidden('Bu randevuya müdahale edemezsiniz.')

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Randevu.STATUS_CHOICES).keys():
            old_status = randevu.status
            randevu.status = new_status
            randevu.save()
            messages.success(request, 'Randevu durumu güncellendi.')
            # E-posta bildirimi gönder
            try:
                subject = 'Randevu Durumunuz Güncellendi'
                body = f"Merhaba {randevu.fullname},\n\nRandevunuzun durumu güncellendi.\n\nPsikolog: {randevu.psychologist}\nTarih: {randevu.date}\nSaat: {randevu.time}\nEski Durum: {old_status}\nYeni Durum: {randevu.get_status_display()}\n\nTeşekkürler, Psyora"
                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [randevu.email])
            except Exception:
                pass
        else:
            messages.error(request, 'Geçersiz durum.')

    return redirect('psikolog_panel')


def psikologlar(request):
    return render(request, 'Psikologlar.html', {'title': 'Psikologlar Sayfası'})
