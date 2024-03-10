from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('open_weather_bot/v1/', include('open_weather_bot.urls')),
]
