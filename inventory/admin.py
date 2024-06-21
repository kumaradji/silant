# inventory/admin.py

from django.contrib import admin
from .models import Machine, Maintenance, Reclamation

admin.site.register(Machine)
admin.site.register(Maintenance)
admin.site.register(Reclamation)
