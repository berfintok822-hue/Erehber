import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Psyora.settings')
import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from Randevular.models import Randevu

c = Client()
username = 'dr_ayse'
password = 'pass1234'
print('Logging in as', username)
if not c.login(username=username, password=password):
    print('Login failed')
    sys.exit(1)

# Find a pending appointment assigned to this psychologist
user = User.objects.get(username=username)
r = Randevu.objects.filter(psychologist_user=user).exclude(status='confirmed').first()
if not r:
    print('No pending appointment found for', username)
    # list existing ones
    for x in Randevu.objects.filter(psychologist_user=user):
        print(x.pk, x.fullname, x.status)
    sys.exit(0)

print('Found randevu:', r.pk, r.fullname, r.status)
# Trigger status update to 'confirmed'
url = f'/randevular/randevu/{r.pk}/durum/'
print('POST', url)
resp = c.post(url, {'status': 'confirmed'}, HTTP_HOST='127.0.0.1:8000')
print('Response status:', resp.status_code)
print('Response content snippet:')
print(resp.content.decode()[:400])

print('Database status now:', Randevu.objects.get(pk=r.pk).status)
