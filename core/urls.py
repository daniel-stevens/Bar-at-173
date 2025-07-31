# bar_at_173/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # include our app's URLs
]

# In development, serve media files through Django
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.kiosk_user_select, name='kiosk-home'),      # Home could be kiosk user selection
    path('kiosk/', views.kiosk_user_select, name='kiosk'),      # explicitly /kiosk path
    path('kiosk/<int:user_id>/', views.kiosk_drink_select, name='kiosk-user-drinks'),
    path('kiosk/<int:user_id>/log/<int:drink_id>/', views.log_consumption, name='log-consumption'),
    path('scoreboard/', views.scoreboard_view, name='scoreboard'),
    path('scoreboard/<int:session_id>/', views.scoreboard_view, name='scoreboard-session'),
]
