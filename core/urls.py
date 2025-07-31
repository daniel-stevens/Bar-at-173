from django.urls import path
from . import views

urlpatterns = [
    path("", views.kiosk_user_select, name="kiosk-home"),
    path("kiosk/", views.kiosk_user_select, name="kiosk"),
    path("kiosk/<int:user_id>/", views.kiosk_drink_select,
         name="kiosk-user-drinks"),
    path("kiosk/<int:user_id>/log/<int:drink_id>/",
         views.log_consumption, name="log-consumption"),
    path("scoreboard/", views.scoreboard_view, name="scoreboard"),
    path("scoreboard/<int:session_id>/",
         views.scoreboard_view, name="scoreboard-session"),
]
