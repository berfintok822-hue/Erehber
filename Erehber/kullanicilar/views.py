from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "POST"])
def kayit_ol(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validasyonlar
        if password != password_confirm:
            messages.error(request, 'Şifreler eşleşmiyor!')
            return render(request, 'kullanicilar/kayit_ol.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Bu kullanıcı adı zaten kullanılıyor!')
            return render(request, 'kullanicilar/kayit_ol.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Bu e-posta zaten kullanılıyor!')
            return render(request, 'kullanicilar/kayit_ol.html')
        
        # Kullanıcı oluştur
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        
        messages.success(request, 'Kayıt başarılı! Giriş yapabilirsiniz.')
        return redirect('login')
    
    return render(request, 'kullanicilar/kayit_ol.html')


@require_http_methods(["GET", "POST"])
def giris_yap(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Hoş geldiniz, {user.first_name or user.username}!')
            
            # Önceki sayfaya yönlendir, yoksa ana sayfaya
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Kullanıcı adı veya şifre yanlış!')
            return render(request, 'kullanicilar/giris_yap.html')
    
    return render(request, 'kullanicilar/giris_yap.html')


@login_required(login_url='login')
def cikis_yap(request):
    logout(request)
    messages.success(request, 'Çıkış yapıldı.')
    return redirect('home')


@login_required(login_url='login')
def profil(request):
    context = {
        'title': 'Profilim'
    }
    return render(request, 'kullanicilar/profil.html', context)
