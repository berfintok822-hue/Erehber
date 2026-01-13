from django.shortcuts import render

# Ana sayfa: Base.html'i render eder, başlık için context sağlar
def home(request):
    return render(request, 'Home.html', {'title': 'Ana Sayfa'})
