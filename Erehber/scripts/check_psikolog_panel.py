import os
import sys
from pathlib import Path

# project root
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Psyora.settings')

import django
django.setup()

from django.test import Client

c = Client()
username = 'dr_ayse'
password = 'pass1234'
print('Attempting login as', username)
logged = c.login(username=username, password=password)
print('login ok:', logged)
resp = c.get('/randevular/psikolog-panel/', HTTP_HOST='127.0.0.1:8000')
print('GET /randevular/psikolog-panel/ status:', resp.status_code)
content = resp.content.decode(errors='ignore')

found_1 = 'Test randevu 1' in content or 'Test User' in content
found_2 = 'Test randevu 2' in content

print('Own appointment present:', found_1)
print('Other doctor appointment present (should be False):', found_2)

# Print a short snippet of page for inspection
start = content.find('<h2>')
end = start + 1000
print('--- page snippet ---')
print(content[start:end])
print('--- end snippet ---')
