import os, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Psyora.settings')
import django
django.setup()
from Randevular.models import Randevu

print('Watcher started — yeni "confirmed" durumlu randevuyu bekliyor... (CTRL+C ile çıkış)')
# baseline confirmed ids
baseline = set(Randevu.objects.filter(status='confirmed').values_list('id', flat=True))
try:
    while True:
        qs = Randevu.objects.filter(status='confirmed').exclude(id__in=baseline).order_by('-updated_at')
        if qs.exists():
            for r in qs:
                print('\n=== New confirmed appointment detected ===')
                print('ID:', r.id)
                print('Fullname:', r.fullname)
                print('Email:', r.email)
                print('Psychologist:', r.psychologist)
                print('Date:', r.date)
                print('Time:', r.time)
                print('Message:', r.message)
                print('Created:', r.created_at)
                print('Updated:', r.updated_at)
                # reconstruct email body same as in views
                print('\n--- Reconstructed email body ---')
                print(f"Merhaba {r.fullname},\n\nRandevunuzun durumu güncellendi.\n\nPsikolog: {r.psychologist}\nTarih: {r.date}\nSaat: {r.time}\nYeni Durum: {r.get_status_display()}\n\nTeşekkürler, Psyora")
                print('--- end ---\n')
            break
        time.sleep(2)
except KeyboardInterrupt:
    print('\nWatcher stopped by user')

print('Watcher exiting')
