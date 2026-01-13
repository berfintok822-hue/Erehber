import os, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Psyora.settings')
import django
django.setup()

from django.contrib.auth.models import User
from Randevular.models import Randevu
from django.core.mail import send_mail
from django.conf import settings

username = 'Muhammedkt'
try:
    user = User.objects.get(username=username)
except User.DoesNotExist:
    print('User not found:', username)
    sys.exit(1)

r = Randevu.objects.filter(psychologist_user=user, status='confirmed').order_by('-updated_at').first()
if not r:
    print('No confirmed appointment found for', username)
    sys.exit(0)

print('Found randevu:')
print('ID:', r.id)
print('Fullname:', r.fullname)
print('Email:', r.email)
print('Psychologist:', r.psychologist)
print('Date:', r.date)
print('Time:', r.time)
print('Status:', r.status)
print('Updated:', r.updated_at)

subject = 'Randevu Durumunuz Güncellendi'
body = f"Merhaba {r.fullname},\n\nRandevunuzun durumu güncellendi.\n\nPsikolog: {r.psychologist}\nTarih: {r.date}\nSaat: {r.time}\nDurum: {r.get_status_display()}\n\nTeşekkürler, Psyora"
print('\nSending email using backend:', settings.EMAIL_BACKEND)
try:
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [r.email])
    print('send_mail called successfully (check console or SMTP)')
except Exception as e:
    print('send_mail error:', e)
