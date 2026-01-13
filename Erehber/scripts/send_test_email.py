import os, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Psyora.settings')
import django
django.setup()
from django.core.mail import send_mail
from django.conf import settings

print('EMAIL_BACKEND =', settings.EMAIL_BACKEND)
print('DEFAULT_FROM_EMAIL =', settings.DEFAULT_FROM_EMAIL)

try:
    send_mail('Test E-posta', 'Bu bir test e-postasıdır.', settings.DEFAULT_FROM_EMAIL, ['test@example.com'])
    print('send_mail executed (check console or SMTP)')
except Exception as e:
    print('send_mail error:', e)
