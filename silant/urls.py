# silant/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from inventory import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls')),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', LogoutView.as_view(next_page='welcome'), name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
