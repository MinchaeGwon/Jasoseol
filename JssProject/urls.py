from django.contrib import admin
from django.urls import path
from main.views import home, create

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('create/', create, name="create"),
]
