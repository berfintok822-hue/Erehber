import os
import sys
from pathlib import Path
import django

# Ensure project root is on path so Django settings module can be imported
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Psyora.settings')
django.setup()

from django.contrib.auth.models import User
from Randevular.models import PsychologistProfile, Randevu


def create_user(username, email, first, last, pwd):
    user, created = User.objects.get_or_create(username=username, defaults={'email': email, 'first_name': first, 'last_name': last})
    if created:
        user.set_password(pwd)
        user.save()
    return user


# Create psychologists
p1 = create_user('dr_ayse', 'ayse@example.com', 'Ayşe', 'Demir', 'pass1234')
PsychologistProfile.objects.get_or_create(user=p1, defaults={'title': 'Dr. Ayşe Demir', 'bio': 'Test psikolog', 'phone': '05320000001', 'active': True})

p2 = create_user('fatih', 'fatih@example.com', 'Fatih', 'Yılmaz', 'pass1234')
PsychologistProfile.objects.get_or_create(user=p2, defaults={'title': 'Uzm. Psikolog Fatih Yılmaz', 'bio': 'Test psikolog', 'phone': '05320000002', 'active': True})

# Create a normal test user
u = create_user('testuser', 'test@example.com', 'Test', 'User', 'testpass')

# Create sample appointments
Randevu.objects.create(user=u, fullname='Test User', email='test@example.com', phone='05550000000', psychologist='Dr. Ayşe Demir', psychologist_user=p1, date='2025-12-25', time='10:00', message='Test randevu 1', status='pending')
Randevu.objects.create(user=u, fullname='Test User', email='test@example.com', phone='05550000000', psychologist='Uzm. Psikolog Fatih Yılmaz', psychologist_user=p2, date='2025-12-26', time='11:00', message='Test randevu 2', status='confirmed')

print('Test data created: users dr_ayse, fatih, testuser and 2 appointments')
