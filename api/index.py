import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the project root to sys.path
# In Vercel, the project root is one level up from 'api'
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coopconnect.settings')

app = get_wsgi_application()
